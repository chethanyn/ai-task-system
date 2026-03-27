from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from models.task import Task
from schemas.task import TaskCreate, TaskUpdate
from utils.deps import admin_only, user_only
from utils.logger import log_activity   # ✅ logging import
from schemas.task import TaskCreate, TaskUpdate, TaskResponse
from typing import List

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🧑‍💼 Admin: Create Task
@router.post("/", response_model=TaskResponse)
def create_task(task: TaskCreate, db: Session = Depends(get_db), user=Depends(admin_only)):
    new_task = Task(
        title=task.title,
        description=task.description,
        assigned_to=task.assigned_to,
        created_by=user.id
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    log_activity(db, user.id, f"Created task {new_task.id}")

    return new_task  

# 👤 User: View Tasks

@router.get("/", response_model=List[TaskResponse])
def get_tasks(db: Session = Depends(get_db), user=Depends(user_only)):
    tasks = db.query(Task).filter(Task.assigned_to == user.id).all()
    return tasks


# 👤 User: Update Task Status
@router.put("/{task_id}")
def update_task(task_id: int, task: TaskUpdate, db: Session = Depends(get_db), user=Depends(user_only)):
    db_task = db.query(Task).filter(
        Task.id == task_id,
        Task.assigned_to == user.id
    ).first()

    if not db_task:
        raise HTTPException(status_code=404, detail="Task not found")

    db_task.status = task.status
    db.commit()

    # ✅ Activity Log
    log_activity(db, user.id, f"Updated task {task_id} to {task.status}")

    return {"message": "Task updated"}


# 🔍 Filtering API (MANDATORY)
@router.get("/filter/", response_model=List[TaskResponse])
def filter_tasks(status: str = None, assigned_to: int = None, db: Session = Depends(get_db)):
    query = db.query(Task)

    if status:
        query = query.filter(Task.status == status)

    if assigned_to:
        query = query.filter(Task.assigned_to == assigned_to)

    return query.all()