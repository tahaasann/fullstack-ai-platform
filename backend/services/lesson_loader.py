import os
import re
import json
import yaml

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "content")


def _safe_path(base_dir: str, relative_path: str) -> str:
    """Validate that the resolved path stays within the base directory."""
    full_path = os.path.realpath(os.path.join(base_dir, relative_path))
    if not full_path.startswith(os.path.realpath(base_dir)):
        raise ValueError(f"Path traversal detected: {relative_path}")
    return full_path


def parse_frontmatter(content: str) -> tuple[dict, str]:
    """Parse YAML frontmatter from markdown content."""
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            try:
                meta = yaml.safe_load(parts[1])
                return meta or {}, parts[2].strip()
            except yaml.YAMLError:
                pass
    return {}, content


def parse_directive(block: str) -> dict:
    """Parse a custom directive block like :::concept[Term] or :::warning."""
    lines = block.strip().split("\n")
    header = lines[0]
    body = "\n".join(lines[1:]).strip()

    # Match :::type[label]{options}
    match = re.match(r"^:::(\w[\w-]*)\[?([^\]]*)\]?\{?([^}]*)\}?", header)
    if not match:
        return {"type": "text", "content": block}

    dtype = match.group(1)
    label = match.group(2).strip() if match.group(2) else ""
    options_str = match.group(3).strip() if match.group(3) else ""

    # Parse options like title="something"
    options = {}
    if options_str:
        for opt_match in re.finditer(r'(\w+)="([^"]*)"', options_str):
            options[opt_match.group(1)] = opt_match.group(2)

    section = {"type": dtype, "content": body}
    if label:
        section["label"] = label
    if options:
        section.update(options)

    # Special parsing for knowledge-check
    if dtype == "knowledge-check":
        section = parse_knowledge_check(body)
        section["type"] = "knowledge_check"

    # Special parsing for comparison tables
    if dtype == "comparison":
        section["type"] = "comparison"
        section["content"] = body

    # Special parsing for architecture diagrams
    if dtype == "architecture":
        section["type"] = "architecture"
        # First line of body can be description (non-code line)
        body_lines = body.split("\n")
        desc_lines = []
        diagram_lines = []
        in_diagram = False
        for line in body_lines:
            if not in_diagram and (line.startswith("┌") or line.startswith("╔") or line.startswith("+") or line.startswith("│") or line.startswith("║") or line.startswith("|") or line.startswith("[") or line.strip().startswith("Client")):
                in_diagram = True
            if in_diagram:
                diagram_lines.append(line)
            else:
                desc_lines.append(line)
        if diagram_lines:
            section["description"] = "\n".join(desc_lines).strip()
            section["content"] = "\n".join(diagram_lines)
        if label:
            section["title"] = label

    return section


def parse_knowledge_check(body: str) -> dict:
    """Parse YAML-like knowledge check content."""
    result = {}
    try:
        data = yaml.safe_load(body)
        if isinstance(data, dict):
            return data
    except yaml.YAMLError:
        pass

    # Fallback: parse line by line
    result["question"] = ""
    result["options"] = []
    result["correct"] = 0
    result["explanation"] = ""

    for line in body.split("\n"):
        line = line.strip()
        if line.startswith("question:"):
            result["question"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("correct:"):
            try:
                result["correct"] = int(line.split(":", 1)[1].strip())
            except ValueError:
                pass
        elif line.startswith("explanation:"):
            result["explanation"] = line.split(":", 1)[1].strip().strip('"')
        elif line.startswith("- "):
            opt = line[2:].strip().strip('"')
            if opt:
                result["options"].append(opt)

    return result


def parse_lesson_content(content_path: str) -> dict:
    """Parse a lesson markdown file into structured sections."""
    full_path = _safe_path(CONTENT_DIR, content_path)

    if not os.path.exists(full_path):
        return {"sections": [], "error": f"File not found: {content_path}"}

    with open(full_path, "r", encoding="utf-8") as f:
        raw = f.read()

    meta, body = parse_frontmatter(raw)
    sections = []

    # Split by directive blocks
    parts = re.split(r"(^:::[\w-]+.*?^:::$)", body, flags=re.MULTILINE | re.DOTALL)

    for part in parts:
        part = part.strip()
        if not part:
            continue

        if part.startswith(":::") and part.endswith(":::"):
            # Remove closing :::
            inner = part[:-3].strip()
            section = parse_directive(inner)
            sections.append(section)
        elif part.startswith(":::"):
            # Directive without closing (single line or unclosed)
            section = parse_directive(part)
            sections.append(section)
        else:
            # Regular markdown content
            # Split by headings for better structure
            heading_parts = re.split(r"(^#{1,6}\s+.+$)", part, flags=re.MULTILINE)
            for hp in heading_parts:
                hp = hp.strip()
                if not hp:
                    continue
                heading_match = re.match(r"^(#{1,6})\s+(.+)$", hp)
                if heading_match:
                    level = len(heading_match.group(1))
                    sections.append({
                        "type": "heading",
                        "level": level,
                        "text": heading_match.group(2)
                    })
                else:
                    sections.append({
                        "type": "markdown",
                        "content": hp
                    })

    return {
        "meta": meta,
        "sections": sections
    }


def load_quiz_content(content_path: str) -> dict:
    """Load quiz JSON file."""
    full_path = _safe_path(CONTENT_DIR, content_path)
    if not os.path.exists(full_path):
        return {"questions": [], "error": f"File not found: {content_path}"}

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_challenge_content(content_path: str) -> dict:
    """Load challenge JSON file."""
    full_path = _safe_path(CONTENT_DIR, content_path)
    if not os.path.exists(full_path):
        return {"error": f"File not found: {content_path}"}

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)


def load_project_content(content_path: str) -> dict:
    """Load project JSON file."""
    full_path = _safe_path(CONTENT_DIR, content_path)
    if not os.path.exists(full_path):
        return {"error": f"File not found: {content_path}"}

    with open(full_path, "r", encoding="utf-8") as f:
        return json.load(f)
