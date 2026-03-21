from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from database import get_db
from models import Phase, Module, Lesson, LessonProgress
from schemas import (
    PhaseOut, PhaseDetailOut, PhaseModuleItem,
    ModuleDetailOut, LessonListItem, LessonDetailOut, ReindexResponse,
)
from services.lesson_loader import parse_lesson_content
from services.content_indexer import index_content
import json

router = APIRouter()


@router.get("/phases", response_model=list[PhaseOut])
def get_phases(db: Session = Depends(get_db)) -> list[PhaseOut]:
    """Return all phases with completion stats."""
    phases = db.query(Phase).options(
        selectinload(Phase.modules).selectinload(Module.lessons)
    ).order_by(Phase.order_index).all()

    # Get all progress in one query
    all_progress = db.query(LessonProgress).all()
    progress_map = {p.lesson_id: p for p in all_progress}

    result = []
    for phase in phases:
        total_lessons = 0
        completed_lessons = 0
        for mod in phase.modules:
            total_lessons += len(mod.lessons)
            for lesson in mod.lessons:
                prog = progress_map.get(lesson.id)
                if prog and prog.status == "completed":
                    completed_lessons += 1

        result.append(PhaseOut(
            id=phase.id,
            title=phase.title,
            description=phase.description,
            order_index=phase.order_index,
            estimated_weeks=phase.estimated_weeks,
            icon=phase.icon,
            module_count=len(phase.modules),
            completed_lessons=completed_lessons,
            total_lessons=total_lessons,
        ))
    return result


@router.get("/phases/{phase_id}", response_model=PhaseDetailOut)
def get_phase(phase_id: str, db: Session = Depends(get_db)) -> PhaseDetailOut:
    """Return phase detail with its modules."""
    phase = db.query(Phase).options(
        selectinload(Phase.modules).selectinload(Module.lessons)
    ).filter(Phase.id == phase_id).first()
    if not phase:
        raise HTTPException(status_code=404, detail="Phase not found")

    # Get all progress for lessons in this phase in one query
    lesson_ids = [l.id for mod in phase.modules for l in mod.lessons]
    progress_list = db.query(LessonProgress).filter(
        LessonProgress.lesson_id.in_(lesson_ids)
    ).all() if lesson_ids else []
    progress_map = {p.lesson_id: p for p in progress_list}

    module_list = []
    for mod in sorted(phase.modules, key=lambda m: m.order_index):
        completed = sum(
            1 for l in mod.lessons
            if progress_map.get(l.id) and progress_map[l.id].status == "completed"
        )
        module_list.append(PhaseModuleItem(
            id=mod.id,
            title=mod.title,
            description=mod.description,
            order_index=mod.order_index,
            estimated_hours=mod.estimated_hours,
            lesson_count=len(mod.lessons),
            completed_lessons=completed,
        ))

    return PhaseDetailOut(
        id=phase.id,
        title=phase.title,
        description=phase.description,
        order_index=phase.order_index,
        estimated_weeks=phase.estimated_weeks,
        icon=phase.icon,
        modules=module_list,
    )


@router.get("/modules/{module_id}", response_model=ModuleDetailOut)
def get_module(module_id: str, db: Session = Depends(get_db)) -> ModuleDetailOut:
    """Return module detail with its lessons and progress."""
    module = db.query(Module).options(
        selectinload(Module.lessons)
    ).filter(Module.id == module_id).first()
    if not module:
        raise HTTPException(status_code=404, detail="Module not found")

    # Get all progress for lessons in this module in one query
    lesson_ids = [l.id for l in module.lessons]
    progress_list = db.query(LessonProgress).filter(
        LessonProgress.lesson_id.in_(lesson_ids)
    ).all() if lesson_ids else []
    progress_map = {p.lesson_id: p for p in progress_list}

    lesson_list = []
    for lesson in sorted(module.lessons, key=lambda l: l.order_index):
        prog = progress_map.get(lesson.id)
        lesson_list.append(LessonListItem(
            id=lesson.id,
            title=lesson.title,
            description=lesson.description,
            order_index=lesson.order_index,
            estimated_minutes=lesson.estimated_minutes,
            tags=json.loads(lesson.tags) if lesson.tags else [],
            status=prog.status if prog else "not_started",
        ))

    return ModuleDetailOut(
        id=module.id,
        phase_id=module.phase_id,
        title=module.title,
        description=module.description,
        estimated_hours=module.estimated_hours,
        lessons=lesson_list,
    )


@router.get("/lessons/{lesson_id:path}", response_model=LessonDetailOut)
def get_lesson(lesson_id: str, db: Session = Depends(get_db)) -> LessonDetailOut:
    """Return full lesson content for the lesson viewer."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found")

    # Parse content
    content = parse_lesson_content(lesson.content_path)

    # Get progress
    prog = db.query(LessonProgress).filter(LessonProgress.lesson_id == lesson_id).first()

    # Get adjacent lessons
    module_lessons = db.query(Lesson).filter(
        Lesson.module_id == lesson.module_id
    ).order_by(Lesson.order_index).all()

    lesson_ids = [l.id for l in module_lessons]
    idx = lesson_ids.index(lesson_id) if lesson_id in lesson_ids else -1
    prev_id = lesson_ids[idx - 1] if idx > 0 else None
    next_id = lesson_ids[idx + 1] if idx < len(lesson_ids) - 1 else None

    return LessonDetailOut(
        id=lesson.id,
        title=lesson.title,
        module_id=lesson.module_id,
        estimated_minutes=lesson.estimated_minutes,
        tags=json.loads(lesson.tags) if lesson.tags else [],
        sections=content.get("sections", []),
        meta=content.get("meta", {}),
        status=prog.status if prog else "not_started",
        time_spent_seconds=prog.time_spent_seconds if prog else 0,
        prev_lesson_id=prev_id,
        next_lesson_id=next_id,
    )


@router.post("/reindex", response_model=ReindexResponse)
def reindex_content(db: Session = Depends(get_db)) -> ReindexResponse:
    """Re-scan content directory and update database."""
    index_content(db)
    return ReindexResponse(status="ok", message="Content re-indexed")
