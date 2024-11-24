from .Base import BaseModel
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
    Uuid
)
from sqlalchemy.orm import relationship
class SchemaModel(BaseModel):
    __tablename__ = "schemas"
    name = Column(String, comment="name of the type")
    query_type_id = Column(Uuid, index=True, nullable=True, comment="name of type repesenting query root")
    mutation_type_id = Column(Uuid, index=True, nullable=True, comment="name of type repesenting mutation root")
