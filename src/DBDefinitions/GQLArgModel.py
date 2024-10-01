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

class GQLArgModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "args"

    name = Column(String, comment="name of the group")
    typeof_id = Column(ForeignKey("types.id"), index=True, comment="typeOf")
   
    typeof = relationship("GQLTypeModel", viewonly=True)
