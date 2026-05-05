from sqlalchemy import Column, Integer, String

from app.database import Base


class Pantry(Base):
    __tablename__ = "pantry"

    id = Column(Integer, primary_key=True, index=True)
    ingredient = Column(String, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
