from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from utils.embeddings import get_embedding
from utils.vector_store import search
from models.document import Document
from utils.logger import log_activity

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/")
def search_docs(query: str, db: Session = Depends(get_db)):
    try:
        embedding = get_embedding(str(query))

        doc_ids = search(embedding)

        results = []

        for doc_id in doc_ids:
            doc = db.query(Document).filter(Document.id == doc_id).first()

            if doc:
                results.append({
                    "id": doc.id,
                    "filename": doc.filename
                })

        # log_activity(db, 0, f"Search query: {query}")

        return {"results": results}

    except Exception as e:
        return {"error": str(e)}