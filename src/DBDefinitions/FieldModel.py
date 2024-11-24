import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .Base import BaseModel

class FieldModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "fields"

    name = Column(String, comment="name of the group")
    description = Column(String, comment="description of the type")

    oftype_id = Column(ForeignKey("types.id"), index=True, nullable=True, comment="typeOf")
    master_type_id = Column(ForeignKey("types.id"), index=True, comment="typeOf")
   
    typeof = relationship("TypeModel", foreign_keys=[oftype_id], viewonly=True)
