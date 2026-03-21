import os
import json
from sqlalchemy.orm import Session
from models import Phase, Module, Lesson, Quiz, Challenge, Project, ProjectMilestone
from utils.logger import get_logger

logger = get_logger(__name__)

CONTENT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "content")


def index_content(db: Session):
    """Scan content directory and populate database with curriculum structure."""
    curriculum_path = os.path.join(CONTENT_DIR, "curriculum.json")
    if not os.path.exists(curriculum_path):
        logger.info("curriculum.json not found, skipping indexing")
        return

    with open(curriculum_path, "r", encoding="utf-8") as f:
        curriculum = json.load(f)

    # Index phases
    for phase_data in curriculum.get("phases", []):
        phase = db.query(Phase).filter(Phase.id == phase_data["id"]).first()
        if not phase:
            phase = Phase(
                id=phase_data["id"],
                title=phase_data["title"],
                description=phase_data.get("description", ""),
                order_index=phase_data["order_index"],
                estimated_weeks=phase_data.get("estimated_weeks", ""),
                icon=phase_data.get("icon", "")
            )
            db.add(phase)
        else:
            phase.title = phase_data["title"]
            phase.description = phase_data.get("description", "")
            phase.order_index = phase_data["order_index"]

        # Index modules
        for mod_data in phase_data.get("modules", []):
            module = db.query(Module).filter(Module.id == mod_data["id"]).first()
            if not module:
                module = Module(
                    id=mod_data["id"],
                    phase_id=phase_data["id"],
                    title=mod_data["title"],
                    description=mod_data.get("description", ""),
                    order_index=mod_data["order_index"],
                    estimated_hours=mod_data.get("estimated_hours", 0),
                    prerequisites=json.dumps(mod_data.get("prerequisites", []))
                )
                db.add(module)
            else:
                module.title = mod_data["title"]
                module.description = mod_data.get("description", "")

            # Index lessons
            for lesson_data in mod_data.get("lessons", []):
                lesson = db.query(Lesson).filter(Lesson.id == lesson_data["id"]).first()
                if not lesson:
                    lesson = Lesson(
                        id=lesson_data["id"],
                        module_id=mod_data["id"],
                        title=lesson_data["title"],
                        description=lesson_data.get("description", ""),
                        order_index=lesson_data["order_index"],
                        content_path=lesson_data["content_path"],
                        estimated_minutes=lesson_data.get("estimated_minutes", 30),
                        tags=json.dumps(lesson_data.get("tags", []))
                    )
                    db.add(lesson)

            # Index quizzes
            for quiz_data in mod_data.get("quizzes", []):
                quiz = db.query(Quiz).filter(Quiz.id == quiz_data["id"]).first()
                if not quiz:
                    quiz = Quiz(
                        id=quiz_data["id"],
                        module_id=mod_data["id"],
                        after_lesson_id=quiz_data.get("after_lesson_id"),
                        title=quiz_data["title"],
                        description=quiz_data.get("description", ""),
                        passing_score=quiz_data.get("passing_score", 70),
                        content_path=quiz_data["content_path"],
                        order_index=quiz_data.get("order_index", 0)
                    )
                    db.add(quiz)

            # Index challenges
            for ch_data in mod_data.get("challenges", []):
                challenge = db.query(Challenge).filter(Challenge.id == ch_data["id"]).first()
                if not challenge:
                    challenge = Challenge(
                        id=ch_data["id"],
                        module_id=mod_data["id"],
                        title=ch_data["title"],
                        description=ch_data.get("description", ""),
                        difficulty=ch_data.get("difficulty", "kolay"),
                        category=ch_data.get("category", ""),
                        content_path=ch_data["content_path"],
                        related_lesson_id=ch_data.get("related_lesson_id"),
                        order_index=ch_data.get("order_index", 0),
                        tags=json.dumps(ch_data.get("tags", []))
                    )
                    db.add(challenge)

    # Index projects
    for proj_data in curriculum.get("projects", []):
        project = db.query(Project).filter(Project.id == proj_data["id"]).first()
        if not project:
            project = Project(
                id=proj_data["id"],
                title=proj_data["title"],
                description=proj_data.get("description", ""),
                order_index=proj_data["order_index"],
                difficulty=proj_data.get("difficulty", ""),
                estimated_days=proj_data.get("estimated_days", 7),
                content_path=proj_data.get("content_path", ""),
                required_phases=json.dumps(proj_data.get("required_phases", [])),
                tech_stack=json.dumps(proj_data.get("tech_stack", []))
            )
            db.add(project)

        for idx, ms_data in enumerate(proj_data.get("milestones", [])):
            milestone = db.query(ProjectMilestone).filter(ProjectMilestone.id == ms_data["id"]).first()
            if not milestone:
                milestone = ProjectMilestone(
                    id=ms_data["id"],
                    project_id=proj_data["id"],
                    title=ms_data["title"],
                    description=ms_data.get("description", ""),
                    order_index=ms_data.get("order_index", idx),
                    content_path=ms_data.get("content_path", ""),
                    checklist=json.dumps(ms_data.get("checklist", []))
                )
                db.add(milestone)

    db.commit()
    logger.info("Content indexed successfully!")
