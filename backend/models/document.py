from sqlalchemy import Column, Integer, String, Text, ForeignKey
from database import Base

class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255))
    content = Column(Text)
    uploaded_by = Column(Integer, ForeignKey("users.id"))