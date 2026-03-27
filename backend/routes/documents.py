from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.document import Document
from utils.deps import admin_only
from utils.logger import log_activity

from utils.embeddings import get_embedding
from utils.vector_store import add_to_index

router = APIRouter()

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 📄 Upload Document (Admin only)
@router.post("/")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    user=Depends(admin_only)
):
    content = file.file.read().decode("utf-8")

    new_doc = Document(
        filename=file.filename,
        content=content,
        uploaded_by=user.id
    )

    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    # 🔥 AI embedding + FAISS
    embedding = get_embedding(content)
    add_to_index(embedding, new_doc.id)

    # ✅ LOG HERE (correct place)
    log_activity(db, user.id, f"Uploaded document {file.filename}")

    print("Document uploaded:", new_doc.id)

    return {
        "message": "Document uploaded",
        "id": new_doc.id
    }