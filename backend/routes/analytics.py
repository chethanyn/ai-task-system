from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.task import Task
from models.user import User
from models.document import Document

router = APIRouter()

# DB connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📊 ANALYTICS API
@router.get("/")
def get_analytics(db: Session = Depends(get_db)):

    total_tasks = db.query(Task).count()
    completed_tasks = db.query(Task).filter(Task.status == "completed").count()
    pending_tasks = db.query(Task).filter(Task.status == "pending").count()

    total_users = db.query(User).count()
    total_documents = db.query(Document).count()

    return {
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "total_users": total_users,
        "total_documents": total_documents
    }