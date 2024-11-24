import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

from .Base import BaseModel

class InputValueModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "args"

    name = Column(String, comment="name of the group")
    description = Column(String, comment="description of the type")

    oftype_id = Column(ForeignKey("types.id"), index=True, nullable=True, comment="typeOf")
    field_id = Column(ForeignKey("fields.id"), index=True, comment="field where arg is placed")
   
    typeof = relationship("TypeModel", viewonly=True)   
