from sqlalchemy import Column, String, Integer

from .database import Base

class SubmittedCode(Base):
    __tablename__ = "submitted_code"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, index=True)
    output = Column(String, index=True)