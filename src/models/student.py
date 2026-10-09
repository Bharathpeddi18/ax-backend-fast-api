
from sqlalchemy import Column, Integer, String
from src.core.database import Base


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(150), nullable=False)
    class_id = Column(Integer, nullable=False)
    photo_id = Column(String(255), nullable=True)
