import json
import os
from typing import Any
from fastapi import APIRouter, HTTPException

router = APIRouter()

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "content", "career")


def _load_json(filename: str) -> dict[str, Any]:
    path = os.path.realpath(os.path.join(CONTENT_DIR, filename))
    if not path.startswith(os.path.realpath(CONTENT_DIR)):
        raise HTTPException(status_code=400, detail="Invalid file path")
    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail=f"{filename} not found")
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@router.get("/career/linkedin-guide")
def get_linkedin_guide() -> dict[str, Any]:
    """Return LinkedIn profile optimization guide."""
    return _load_json("linkedin-guide.json")


@router.get("/career/cover-letter-templates")
def get_cover_letter_templates() -> dict[str, Any]:
    """Return cover letter templates and examples."""
    return _load_json("cover-letter-templates.json")


@router.get("/career/ai-tools-guide")
def get_ai_tools_guide() -> dict[str, Any]:
    """Return AI tools guide for job search."""
    return _load_json("ai-tools-guide.json")


@router.get("/career/cv-templates")
def get_cv_templates() -> dict[str, Any]:
    """Return CV templates and formatting guides."""
    return _load_json("cv-templates.json")


@router.get("/career/job-search-strategy")
def get_job_search_strategy() -> dict[str, Any]:
    """Return job search strategy guide."""
    return _load_json("job-search-strategy.json")


@router.get("/career/employment-gap-guide")
def get_employment_gap_guide() -> dict[str, Any]:
    """Return employment gap explanation guide."""
    return _load_json("employment-gap-guide.json")


@router.get("/career/github-profile-guide")
def get_github_profile_guide() -> dict[str, Any]:
    """Return GitHub profile optimization guide."""
    return _load_json("github-profile-guide.json")
