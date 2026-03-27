from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal
from schemas.user import UserLogin
from models.user import User
from utils.hash import verify_password
from utils.auth import create_access_token
from utils.deps import admin_only, user_only
from utils.logger import log_activity
from schemas.user import UserCreate
from utils.hash import hash_password

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 🔐 LOGIN API
@router.post("/login")
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()

    if not db_user:
        raise HTTPException(status_code=400, detail="User not found")

    # ✅ IMPORTANT: password verification
    if not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=400, detail="Invalid password")

    # ✅ LOG
    log_activity(db, db_user.id, "User logged in")

    # ✅ TOKEN
    token = create_access_token({"sub": db_user.email})

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@router.post("/register")
def register(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        role_id=2
    )

    db.add(new_user)
    db.commit()

    return {"message": "User created"}

# 🛡️ ADMIN ONLY API
@router.get("/admin-test")
def admin_test(user=Depends(admin_only)):
    return {"message": "Admin access granted"}

# 👤 USER ONLY API
@router.get("/user-test")
def user_test(user=Depends(user_only)):
    return {"message": "User access granted"}