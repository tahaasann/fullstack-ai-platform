import subprocess
import tempfile
import os
import json
import time
from services.lesson_loader import load_challenge_content


def run_challenge(challenge_content_path: str, code: str, language: str = "python",
                  include_hidden: bool = False) -> dict:
    """Run user code against test cases."""
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


def run_python_test(code: str, tc_input: dict, expected, challenge: dict) -> dict:
    """Execute Python code with test input."""
    # Build test harness
    # Find function name from starter code
    starter = challenge.get("starter_code", {}).get("python", "")
    func_name = "solution"
    import re
    match = re.search(r"def\s+(\w+)\s*\(", starter)
    if match:
        func_name = match.group(1)

    # Build argument string
    args = ", ".join(repr(v) for v in tc_input.values())

    test_code = f"""{code}

import json
try:
    result = {func_name}({args})
    print(json.dumps(result))
except Exception as e:
    print(json.dumps({{"__error__": str(e)}}))
"""

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".py", delete=False, encoding="utf-8") as f:
            f.write(test_code)
            tmp_path = f.name

        result = subprocess.run(
            ["python", tmp_path],
            capture_output=True, text=True, timeout=10, encoding="utf-8"
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
        try:
            actual = json.loads(stdout)
        except json.JSONDecodeError:
            actual = stdout

        # Check if error was reported
        if isinstance(actual, dict) and "__error__" in actual:
            return {
                "passed": False,
                "input": str(tc_input),
                "expected": str(expected),
                "actual": None,
                "error": actual["__error__"]
            }

        # Compare (handle sorted lists for order-independent comparison)
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
            "error": "Zaman aşımı (10 saniye)"
        }
    except Exception as e:
        return {
            "passed": False,
            "input": str(tc_input),
            "expected": str(expected),
            "actual": None,
            "error": str(e)
        }


def run_js_test(code: str, tc_input: dict, expected, challenge: dict) -> dict:
    """Execute JavaScript code with test input."""
    starter = challenge.get("starter_code", {}).get("javascript", "")
    import re
    match = re.search(r"function\s+(\w+)\s*\(", starter)
    func_name = match.group(1) if match else "solution"

    args = ", ".join(json.dumps(v) for v in tc_input.values())

    test_code = f"""{code}

try {{
    const result = {func_name}({args});
    console.log(JSON.stringify(result));
}} catch(e) {{
    console.log(JSON.stringify({{"__error__": e.message}}));
}}
"""

    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
            f.write(test_code)
            tmp_path = f.name

        result = subprocess.run(
            ["node", tmp_path],
            capture_output=True, text=True, timeout=10, encoding="utf-8"
        )

        os.unlink(tmp_path)

        if result.returncode != 0:
            return {
                "passed": False, "input": str(tc_input), "expected": str(expected),
                "actual": None, "error": result.stderr.strip().split("\n")[-1] if result.stderr else "Runtime error"
            }

        stdout = result.stdout.strip()
        try:
            actual = json.loads(stdout)
        except json.JSONDecodeError:
            actual = stdout

        if isinstance(actual, dict) and "__error__" in actual:
            return {"passed": False, "input": str(tc_input), "expected": str(expected),
                    "actual": None, "error": actual["__error__"]}

        passed = compare_results(actual, expected)
        return {"passed": passed, "input": str(tc_input), "expected": str(expected),
                "actual": str(actual), "error": None}

    except subprocess.TimeoutExpired:
        try:
            os.unlink(tmp_path)
        except Exception:
            pass
        return {"passed": False, "input": str(tc_input), "expected": str(expected),
                "actual": None, "error": "Zaman aşımı (10 saniye)"}
    except Exception as e:
        return {"passed": False, "input": str(tc_input), "expected": str(expected),
                "actual": None, "error": str(e)}


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
