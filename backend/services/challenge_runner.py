import subprocess
import tempfile
import os
import json
import re
import time
import ast
from services.lesson_loader import load_challenge_content

# --- Constants ---
CHALLENGE_TIMEOUT_SECONDS = 5
MAX_CODE_SIZE_BYTES = 10240
MAX_STDOUT_SIZE = 1_048_576  # 1MB

DANGEROUS_MODULES = {
    "os", "sys", "subprocess", "shutil", "socket", "http", "requests",
    "pathlib", "ctypes", "signal", "importlib", "pickle", "shelve"
}

DANGEROUS_FUNCTIONS = {
    "open", "exec", "eval", "__import__", "compile", "globals", "locals",
    "getattr", "setattr", "delattr", "breakpoint", "input", "exit", "quit"
}


def validate_python_code(code: str) -> tuple[bool, str]:
    """Validate Python code for dangerous imports and function calls using AST.

    Args:
        code: The user-submitted Python source code to validate.

    Returns:
        A tuple of (is_safe, error_message). If is_safe is True,
        error_message is an empty string. If False, error_message
        describes the security violation found.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return (True, "")  # Let syntax errors be caught at runtime

    for node in ast.walk(tree):
        # Check import statements
        if isinstance(node, ast.Import):
            for alias in node.names:
                module_root = alias.name.split(".")[0]
                if module_root in DANGEROUS_MODULES:
                    return (False, f"Güvenlik: '{alias.name}' modülü kullanılamaz")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                module_root = node.module.split(".")[0]
                if module_root in DANGEROUS_MODULES:
                    return (False, f"Güvenlik: '{node.module}' modülü kullanılamaz")
        # Check function calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in DANGEROUS_FUNCTIONS:
                    return (False, f"Güvenlik: '{node.func.id}' fonksiyonu kullanılamaz")
            elif isinstance(node.func, ast.Attribute):
                if node.func.attr in DANGEROUS_FUNCTIONS:
                    return (False, f"Güvenlik: '{node.func.attr}' fonksiyonu kullanılamaz")

    return (True, "")


def validate_js_code(code: str) -> tuple[bool, str]:
    """Validate JavaScript code for dangerous patterns using string matching.

    Args:
        code: The user-submitted JavaScript source code to validate.

    Returns:
        A tuple of (is_safe, error_message). If is_safe is True,
        error_message is an empty string. If False, error_message
        describes the security violation found.
    """
    dangerous_requires = [
        "fs", "child_process", "net", "http", "https", "dgram",
        "cluster", "worker_threads", "os", "path", "vm", "crypto"
    ]

    for mod in dangerous_requires:
        if f"require('{mod}')" in code or f'require("{mod}")' in code:
            return (False, f"Güvenlik: '{mod}' modülü kullanılamaz")
        if f"from '{mod}'" in code or f'from "{mod}"' in code:
            return (False, f"Güvenlik: '{mod}' modülü kullanılamaz")

    dangerous_patterns = ["process.exit", "process.env", "require("]
    for pattern in dangerous_patterns:
        if pattern in code:
            return (False, f"Güvenlik: '{pattern}' kullanılamaz")

    return (True, "")


def run_challenge(challenge_content_path: str, code: str, language: str = "python",
                  include_hidden: bool = False) -> dict:
    """Run user code against all test cases for a challenge.

    Loads the challenge definition, validates the code for security,
    then executes each test case and aggregates results.

    Args:
        challenge_content_path: Path to the challenge YAML/JSON content file.
        code: The user-submitted source code to test.
        language: Programming language, either "python" or "javascript".
        include_hidden: Whether to include hidden test cases in the run.

    Returns:
        A dict with keys: status ("passed"/"failed"/"error"), tests_passed,
        tests_total, results (list of per-test dicts), execution_time_ms.
    """
    if len(code) > MAX_CODE_SIZE_BYTES:
        return {"status": "error", "error": "Kod boyutu çok büyük (max 10KB)", "tests_passed": 0, "tests_total": 0, "results": []}

    challenge = load_challenge_content(challenge_content_path)
    if "error" in challenge:
        return {"status": "error", "error": challenge["error"], "tests_passed": 0, "tests_total": 0, "results": []}

    test_cases = challenge.get("test_cases", [])
    if include_hidden:
        test_cases = test_cases + challenge.get("hidden_test_cases", [])

    results = []
    tests_passed = 0
    start_time = time.time()

    for i, tc in enumerate(test_cases):
        result = run_single_test(code, language, tc, challenge)
        results.append(result)
        if result["passed"]:
            tests_passed += 1

    elapsed_ms = int((time.time() - start_time) * 1000)

    status = "passed" if tests_passed == len(test_cases) else "failed"
    if any(r.get("error") for r in results):
        status = "error"

    return {
        "status": status,
        "tests_passed": tests_passed,
        "tests_total": len(test_cases),
        "results": results,
        "execution_time_ms": elapsed_ms
    }


def run_single_test(code: str, language: str, test_case: dict, challenge: dict) -> dict:
    """Run code against a single test case."""
    tc_input = test_case["input"]
    expected = test_case["expected"]

    if language == "python":
        return run_python_test(code, tc_input, expected, challenge)
    elif language == "javascript":
        return run_js_test(code, tc_input, expected, challenge)
    else:
        return {"passed": False, "error": f"Unsupported language: {language}"}


def _build_python_harness(code: str, func_name: str, args: str) -> str:
    """Build the Python test harness code that wraps user code."""
    return f"""{code}

import json
try:
    result = {func_name}({args})
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({{"__error__": str(e)}}))
"""


def _build_js_harness(code: str, func_name: str, args: str) -> str:
    """Build the JavaScript test harness code that wraps user code."""
    return f"""{code}

try {{
    const result = {func_name}({args});
    console.log(JSON.stringify(result));
}} catch(e) {{
    console.log(JSON.stringify({{"__error__": e.message}}));
}}
"""


def _execute_code(command: list, tmp_path: str, tc_input: dict, expected) -> dict:
    """Execute code in a subprocess and parse the result.

    Common execution logic shared by both Python and JavaScript runners.
    Handles subprocess invocation, timeout, output parsing, error extraction,
    and result comparison.

    Args:
        command: The command list to pass to subprocess.run (e.g. ["python", path]).
        tmp_path: Path to the temporary file containing the test harness code.
        tc_input: The test case input dict (used for error reporting).
        expected: The expected output value for comparison.

    Returns:
        A dict with keys: passed (bool), input, expected, actual, error.
    """
    try:
        result = subprocess.run(
            command,
            capture_output=True, text=True,
            timeout=CHALLENGE_TIMEOUT_SECONDS,
            encoding="utf-8",
            env={"PATH": os.environ.get("PATH", "")}
        )

        os.unlink(tmp_path)

        if result.returncode != 0:
            return {
                "passed": False,
                "input": str(tc_input),
                "expected": str(expected),
                "actual": None,
                "error": result.stderr.strip().split("\n")[-1] if result.stderr else "Runtime error"
            }

        stdout = result.stdout.strip()
        if len(stdout) > MAX_STDOUT_SIZE:
            return {
                "passed": False,
                "input": str(tc_input),
                "expected": str(expected),
                "actual": None,
                "error": "Çıktı boyutu çok büyük (max 1MB)"
            }

        try:
            actual = json.loads(stdout)
        except json.JSONDecodeError:
            actual = stdout

        # Check if error was reported from within the harness
        if isinstance(actual, dict) and "__error__" in actual:
            return {
                "passed": False,
                "input": str(tc_input),
                "expected": str(expected),
                "actual": None,
                "error": actual["__error__"]
            }

        passed = compare_results(actual, expected)

        return {
            "passed": passed,
            "input": str(tc_input),
            "expected": str(expected),
            "actual": str(actual),
            "error": None
        }

    except subprocess.TimeoutExpired:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        return {
            "passed": False,
            "input": str(tc_input),
            "expected": str(expected),
            "actual": None,
            "error": f"Zaman aşımı ({CHALLENGE_TIMEOUT_SECONDS} saniye)"
        }
    except Exception as e:
        return {
            "passed": False,
            "input": str(tc_input),
            "expected": str(expected),
            "actual": None,
            "error": str(e)
        }


def run_python_test(code: str, tc_input: dict, expected, challenge: dict) -> dict:
    """Execute Python code with test input."""
    starter = challenge.get("starter_code", {}).get("python", "")
    func_name = "solution"
    match = re.search(r"def\s+(\w+)\s*\(", starter)
    if match:
        func_name = match.group(1)

    args = ", ".join(repr(v) for v in tc_input.values())

    # Security validation
    is_safe, error_msg = validate_python_code(code)
    if not is_safe:
        return {"passed": False, "input": str(tc_input), "expected": str(expected), "actual": None, "error": error_msg}

    test_code = _build_python_harness(code, func_name, args)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
        f.write(test_code)
        tmp_path = f.name

    return _execute_code(["python", tmp_path], tmp_path, tc_input, expected)


def run_js_test(code: str, tc_input: dict, expected, challenge: dict) -> dict:
    """Execute JavaScript code with test input."""
    starter = challenge.get("starter_code", {}).get("javascript", "")
    match = re.search(r"function\s+(\w+)\s*\(", starter)
    func_name = match.group(1) if match else "solution"

    args = ", ".join(json.dumps(v) for v in tc_input.values())

    # Security validation
    is_safe, error_msg = validate_js_code(code)
    if not is_safe:
        return {"passed": False, "input": str(tc_input), "expected": str(expected), "actual": None, "error": error_msg}

    test_code = _build_js_harness(code, func_name, args)

    with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
        f.write(test_code)
        tmp_path = f.name

    return _execute_code(["node", tmp_path], tmp_path, tc_input, expected)


def compare_results(actual, expected) -> bool:
    """Compare results, handling sorted arrays for order-independent comparison."""
    if actual == expected:
        return True

    # Try sorted comparison for lists
    if isinstance(actual, list) and isinstance(expected, list):
        try:
            return sorted(actual) == sorted(expected)
        except TypeError:
            return False

    # Try string comparison
    return str(actual) == str(expected)
