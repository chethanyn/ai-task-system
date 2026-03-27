from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from database import SessionLocal
from models.user import User

SECRET_KEY = "mysecretkey"
ALGORITHM = "HS256"

security = HTTPBearer()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security), db=Depends(get_db)):
    token = credentials.credentials
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = db.query(User).filter(User.email == email).first()

    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user

def admin_only(user: User = Depends(get_current_user)):
    if user.role_id != 1:
        raise HTTPException(status_code=403, detail="Admin only")
    return user

def user_only(user: User = Depends(get_current_user)):
    if user.role_id != 2:
        raise HTTPException(status_code=403, detail="User only")
    return user