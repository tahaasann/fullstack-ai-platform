"""
Update curriculum.json with milestones extracted from project JSON files.
Run this after generating project-06.json through project-10.json.
"""
import json
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CURRICULUM_PATH = os.path.join(BASE_DIR, "content", "curriculum.json")
PROJECTS_DIR = os.path.join(BASE_DIR, "content", "projects")


def extract_milestones_from_project(project_json_path):
    """Extract milestone checklist items from a project JSON file."""
    with open(project_json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    milestones = data.get("milestones", [])
    result = []
    for ms in milestones:
        ms_id = ms.get("id", "")
        title = ms.get("title", "")
        overview = ms.get("overview", "")
        steps = ms.get("steps", [])
        checklist = [s.get("title", f"Step {s.get('step', '?')}") for s in steps]

        result.append({
            "id": ms_id,
            "title": title,
            "description": overview[:200] if overview else "",
            "checklist": checklist
        })
    return result


def update_curriculum():
    with open(CURRICULUM_PATH, "r", encoding="utf-8") as f:
        curriculum = json.load(f)

    updated = 0
    for project in curriculum.get("projects", []):
        content_path = project.get("content_path", "")
        if not content_path:
            continue

        project_file = os.path.join(BASE_DIR, "content", content_path)
        if not os.path.exists(project_file):
            print(f"  SKIP {content_path} — file not found")
            continue

        # Only update if milestones are empty
        existing_ms = project.get("milestones", [])
        if len(existing_ms) > 0:
            print(f"  SKIP {project['id']} — already has {len(existing_ms)} milestones")
            continue

        milestones = extract_milestones_from_project(project_file)
        if milestones:
            project["milestones"] = milestones
            print(f"  UPDATED {project['id']} — {len(milestones)} milestones added")
            updated += 1
        else:
            print(f"  WARN {project['id']} — no milestones found in {content_path}")

    with open(CURRICULUM_PATH, "w", encoding="utf-8") as f:
        json.dump(curriculum, f, ensure_ascii=False, indent=2)

    print(f"\nDone! Updated {updated} projects.")


if __name__ == "__main__":
    update_curriculum()
