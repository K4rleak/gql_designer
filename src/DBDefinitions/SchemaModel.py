from .Base import BaseModel
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
class SchemaModel(BaseModel):
    __tablename__ = "schemas"
    name = Column(String, comment="name of the type")