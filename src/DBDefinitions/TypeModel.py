import sqlalchemy
from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime,
    Boolean,
)
from sqlalchemy.orm import relationship

from .Base import BaseModel

class TypeModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "types"

    name = Column(String, comment="name of the type")
    description = Column(String, comment="description of the type")
    kind = Column(String, comment="kind of the type aka SCALAR, OBJECT, NON_NULL")
    isDeprecated = Column(Boolean, comment="if it is depreacted", default=False)
    deprecationReason = Column(String, comment="the reason why it is deprecated", nullable=True)

    oftype_id = Column(ForeignKey("types.id"), index=True, nullable=True, comment="typeOf")
    schema_id = Column(ForeignKey("schemas.id"), index=True, comment="schema")

    typeof = relationship("TypeModel", viewonly=True)
