from pydantic import BaseModel

class TaskCreate(BaseModel):
    title: str
    description: str
    assigned_to: int

class TaskUpdate(BaseModel):
    status: str

# 🔥 ADD THIS
class TaskResponse(BaseModel):
    id: int
    title: str
    description: str
    assigned_to: int
    created_by: int
    status: str

    class Config:
        from_attributes = True   # ✅ VERY IMPORTANT