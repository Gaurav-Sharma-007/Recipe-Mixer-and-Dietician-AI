from sqlalchemy import Column, Integer, String, Text, ForeignKey
from app.database import Base


class Recipe(Base):
    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    # optional but useful
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)