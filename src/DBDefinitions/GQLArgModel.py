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
    """Spravuje data spojena s argumenty"""

    __tablename__ = "args"

    name = Column(String, comment="name of the arg")
    description = Column(String, comment="description")
    default_value = Column(String, comment="default value written as a string")
    typeof_id = Column(ForeignKey("types.id"), index=True, comment="typeOf")
   
    typeof = relationship("GQLTypeModel", viewonly=True)
