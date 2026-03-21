from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Literal
from database import get_db
from models import Bookmark, Lesson, Challenge, Project
from schemas import BookmarkOut, BookmarkCheck, BookmarkCreateResponse, BookmarkDeleteResponse

router = APIRouter()


@router.get("/bookmarks", response_model=list[BookmarkOut])
def list_bookmarks(db: Session = Depends(get_db)) -> list[BookmarkOut]:
    """Return all bookmarks with resolved item titles."""
    bookmarks = db.query(Bookmark).order_by(Bookmark.created_at.desc()).all()

    # Group bookmark item_ids by type
    ids_by_type: dict[str, list[str]] = {}
    for b in bookmarks:
        ids_by_type.setdefault(b.item_type, []).append(b.item_id)

    # Batch query each type
    resolved: dict[tuple[str, str], dict] = {}
    if "lesson" in ids_by_type:
        for lesson in db.query(Lesson).filter(Lesson.id.in_(ids_by_type["lesson"])).all():
            resolved[("lesson", lesson.id)] = {"title": lesson.title, "link": f"/lesson/{lesson.id}"}
    if "challenge" in ids_by_type:
        for ch in db.query(Challenge).filter(Challenge.id.in_(ids_by_type["challenge"])).all():
            resolved[("challenge", ch.id)] = {"title": ch.title, "link": f"/challenge/{ch.id}"}
    if "project" in ids_by_type:
        for proj in db.query(Project).filter(Project.id.in_(ids_by_type["project"])).all():
            resolved[("project", proj.id)] = {"title": proj.title, "link": f"/project/{proj.id}"}

    result = []
    for b in bookmarks:
        item = resolved.get((b.item_type, b.item_id))
        result.append(BookmarkOut(
            id=b.id,
            item_type=b.item_type,
            item_id=b.item_id,
            note=b.note,
            created_at=b.created_at.isoformat() if b.created_at else None,
            title=item.get("title", b.item_id) if item else b.item_id,
            link=item.get("link", "") if item else "",
        ))
    return result


@router.get("/bookmarks/check", response_model=BookmarkCheck)
def check_bookmark(item_type: Literal["lesson", "challenge", "project"], item_id: str, db: Session = Depends(get_db)) -> BookmarkCheck:
    """Check if an item is bookmarked."""
    b = db.query(Bookmark).filter(
        Bookmark.item_type == item_type,
        Bookmark.item_id == item_id
    ).first()
    return BookmarkCheck(bookmarked=b is not None, id=b.id if b else None)


@router.post("/bookmarks", response_model=BookmarkCreateResponse)
def create_bookmark(item_type: Literal["lesson", "challenge", "project"], item_id: str, note: str = Query(default="", max_length=500), db: Session = Depends(get_db)) -> BookmarkCreateResponse:
    """Create a bookmark for an item."""
    existing = db.query(Bookmark).filter(
        Bookmark.item_type == item_type,
        Bookmark.item_id == item_id
    ).first()
    if existing:
        return BookmarkCreateResponse(id=existing.id, message="already bookmarked")

    b = Bookmark(item_type=item_type, item_id=item_id, note=note or None)
    db.add(b)
    db.commit()
    db.refresh(b)
    return BookmarkCreateResponse(id=b.id, message="bookmarked")


@router.delete("/bookmarks/{bookmark_id}", response_model=BookmarkDeleteResponse)
def delete_bookmark(bookmark_id: int, db: Session = Depends(get_db)) -> BookmarkDeleteResponse:
    """Delete a bookmark."""
    b = db.query(Bookmark).filter(Bookmark.id == bookmark_id).first()
    if not b:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    db.delete(b)
    db.commit()
    return BookmarkDeleteResponse(message="deleted")


def _resolve_item(db: Session, item_type: str, item_id: str) -> dict | None:
    if item_type == "lesson":
        lesson = db.query(Lesson).filter(Lesson.id == item_id).first()
        if lesson:
            return {"title": lesson.title, "link": f"/lesson/{item_id}"}
    elif item_type == "challenge":
        ch = db.query(Challenge).filter(Challenge.id == item_id).first()
        if ch:
            return {"title": ch.title, "link": f"/challenge/{item_id}"}
    elif item_type == "project":
        proj = db.query(Project).filter(Project.id == item_id).first()
        if proj:
            return {"title": proj.title, "link": f"/project/{item_id}"}
    return None
