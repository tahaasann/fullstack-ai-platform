from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from models import Project, ProjectMilestone, ProjectProgress, MilestoneProgress
from schemas import (
    ProjectListItem, ProjectCvGuidanceItem, ProjectDetailOut,
    MilestoneDetailItem, StatusResponse, CompletedResponse,
    RepoUrlResponse, ChecklistStateResponse,
)
from services.lesson_loader import load_project_content
from datetime import datetime, timezone
import json

router = APIRouter()


@router.get("/projects", response_model=list[ProjectListItem])
def list_projects(db: Session = Depends(get_db)) -> list[ProjectListItem]:
    """Return all projects with progress stats."""
    projects = db.query(Project).order_by(Project.order_index).all()
    project_ids = [p.id for p in projects]

    # Batch query all related data
    progress_map = {pp.project_id: pp for pp in
        db.query(ProjectProgress).filter(ProjectProgress.project_id.in_(project_ids)).all()}

    all_milestones = db.query(ProjectMilestone).filter(
        ProjectMilestone.project_id.in_(project_ids)).all()
    milestone_ids = [m.id for m in all_milestones]

    completed_ms_ids = set(mp.milestone_id for mp in
        db.query(MilestoneProgress).filter(
            MilestoneProgress.milestone_id.in_(milestone_ids),
            MilestoneProgress.completed == True).all()) if milestone_ids else set()

    milestones_by_project = {}
    for m in all_milestones:
        milestones_by_project.setdefault(m.project_id, []).append(m)

    result = []
    for p in projects:
        prog = progress_map.get(p.id)
        ms_list = milestones_by_project.get(p.id, [])
        completed_ms = sum(1 for ms in ms_list if ms.id in completed_ms_ids)
        result.append(ProjectListItem(
            id=p.id,
            title=p.title,
            description=p.description,
            order_index=p.order_index,
            difficulty=p.difficulty,
            estimated_days=p.estimated_days,
            tech_stack=json.loads(p.tech_stack) if p.tech_stack else [],
            status=prog.status if prog else "not_started",
            completed_milestones=completed_ms,
            total_milestones=len(ms_list),
        ))
    return result


@router.get("/projects/cv-guidance", response_model=list[ProjectCvGuidanceItem])
def get_all_cv_guidance(db: Session = Depends(get_db)) -> list[ProjectCvGuidanceItem]:
    """Return CV and GitHub guidance for all projects."""
    projects = db.query(Project).order_by(Project.order_index).all()
    results = []
    for p in projects:
        content = {}
        if p.content_path:
            content = load_project_content(p.content_path)
        results.append(ProjectCvGuidanceItem(
            project_id=p.id,
            project_title=p.title,
            cv_guidance=content.get("cv_guidance"),
            github_guidance=content.get("github_guidance"),
        ))
    return results


@router.get("/projects/{project_id}", response_model=ProjectDetailOut)
def get_project(project_id: str, db: Session = Depends(get_db)) -> ProjectDetailOut:
    """Return full project detail with milestones and content."""
    project = db.query(Project).filter(Project.id == project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    prog = db.query(ProjectProgress).filter(ProjectProgress.project_id == project_id).first()
    milestones = db.query(ProjectMilestone).filter(
        ProjectMilestone.project_id == project_id
    ).order_by(ProjectMilestone.order_index).all()

    milestone_ids = [ms.id for ms in milestones]
    ms_progress_map = {mp.milestone_id: mp for mp in
        db.query(MilestoneProgress).filter(
            MilestoneProgress.milestone_id.in_(milestone_ids)).all()} if milestone_ids else {}

    ms_list = []
    for ms in milestones:
        ms_prog = ms_progress_map.get(ms.id)
        ms_list.append(MilestoneDetailItem(
            id=ms.id,
            title=ms.title,
            description=ms.description,
            order_index=ms.order_index,
            checklist=json.loads(ms.checklist) if ms.checklist else [],
            completed=ms_prog.completed if ms_prog else False,
            checklist_state=json.loads(ms_prog.checklist_state) if ms_prog and ms_prog.checklist_state else None,
        ))

    # Load detailed content if available
    content = {}
    if project.content_path:
        content = load_project_content(project.content_path)

    return ProjectDetailOut(
        id=project.id,
        title=project.title,
        description=project.description,
        difficulty=project.difficulty,
        estimated_days=project.estimated_days,
        tech_stack=json.loads(project.tech_stack) if project.tech_stack else [],
        required_phases=json.loads(project.required_phases) if project.required_phases else [],
        status=prog.status if prog else "not_started",
        repo_url=prog.repo_url if prog else None,
        milestones=ms_list,
        brief=content.get("brief", ""),
        requirements=content.get("requirements", {}),
        resources=content.get("resources", []),
        target_roles=content.get("target_roles", []),
        architecture=content.get("architecture", {}),
        what_you_learn=content.get("what_you_learn", {}),
        evaluation_criteria=content.get("evaluation_criteria", []),
        interview_prep=content.get("interview_prep", {}),
        milestone_details=content.get("milestones", []),
        cv_guidance=content.get("cv_guidance"),
        github_guidance=content.get("github_guidance"),
    )


@router.post("/projects/{project_id}/start", response_model=StatusResponse)
def start_project(project_id: str, db: Session = Depends(get_db)) -> StatusResponse:
    """Start a project."""
    prog = db.query(ProjectProgress).filter(ProjectProgress.project_id == project_id).first()
    if not prog:
        prog = ProjectProgress(
            project_id=project_id,
            status="in_progress",
            started_at=datetime.now(timezone.utc)
        )
        db.add(prog)
    else:
        prog.status = "in_progress"
    db.commit()
    return StatusResponse(status="in_progress")


@router.post("/projects/{project_id}/complete", response_model=StatusResponse)
def complete_project(project_id: str, db: Session = Depends(get_db)) -> StatusResponse:
    """Mark a project as completed."""
    prog = db.query(ProjectProgress).filter(ProjectProgress.project_id == project_id).first()
    if not prog:
        prog = ProjectProgress(
            project_id=project_id,
            status="completed",
            completed_at=datetime.now(timezone.utc)
        )
        db.add(prog)
    else:
        prog.status = "completed"
        prog.completed_at = datetime.now(timezone.utc)
    db.commit()
    return StatusResponse(status="completed")


@router.patch("/projects/{project_id}/repo", response_model=RepoUrlResponse)
def update_repo(project_id: str, repo_url: str, db: Session = Depends(get_db)) -> RepoUrlResponse:
    """Update project repository URL."""
    prog = db.query(ProjectProgress).filter(ProjectProgress.project_id == project_id).first()
    if not prog:
        prog = ProjectProgress(project_id=project_id, status="in_progress", repo_url=repo_url)
        db.add(prog)
    else:
        prog.repo_url = repo_url
    db.commit()
    return RepoUrlResponse(repo_url=repo_url)


@router.post("/milestones/{milestone_id}/toggle", response_model=CompletedResponse)
def toggle_milestone(milestone_id: str, db: Session = Depends(get_db)) -> CompletedResponse:
    """Toggle milestone completion status."""
    prog = db.query(MilestoneProgress).filter(MilestoneProgress.milestone_id == milestone_id).first()
    if not prog:
        prog = MilestoneProgress(
            milestone_id=milestone_id,
            completed=True,
            completed_at=datetime.now(timezone.utc)
        )
        db.add(prog)
    else:
        prog.completed = not prog.completed
        prog.completed_at = datetime.now(timezone.utc) if prog.completed else None
    db.commit()
    return CompletedResponse(completed=prog.completed)


@router.patch("/milestones/{milestone_id}/checklist", response_model=ChecklistStateResponse)
def update_checklist(milestone_id: str, checklist_state: list, db: Session = Depends(get_db)) -> ChecklistStateResponse:
    """Update milestone checklist state."""
    prog = db.query(MilestoneProgress).filter(MilestoneProgress.milestone_id == milestone_id).first()
    if not prog:
        prog = MilestoneProgress(
            milestone_id=milestone_id,
            checklist_state=json.dumps(checklist_state)
        )
        db.add(prog)
    else:
        prog.checklist_state = json.dumps(checklist_state)
    db.commit()
    return ChecklistStateResponse(checklist_state=checklist_state)
