from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models.document import Document
from utils.embeddings import get_embedding
from utils.vector_store import add_to_index

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    content = file.file.read().decode("utf-8")

    new_doc = Document(filename=file.filename)
    db.add(new_doc)
    db.commit()
    db.refresh(new_doc)

    embedding = get_embedding(content)

    add_to_index(embedding, new_doc.id)  # ✅ FIXED

    return {"message": "Document uploaded"}