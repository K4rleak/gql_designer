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

class GQLTypeModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "types"

    name = Column(String, comment="name of the type")
    description = Column(String, comment="description of the type")
    isDeprecated = Column(Boolean, comment="if it is depreacted", default=False)
    deprecationReason = Column(String, comment="the reason why it is deprecated", nullable=True)

    typeof_id = Column(ForeignKey("types.id"), index=True, comment="typeOf")
    typeof = relationship("GQLTypeModel", viewonly=True)

    kind = Column(String, comment="kind of the type aka SCALAR, OBJECT, NON_NULL")
    #kind = Column(ForeignKey("types.id"), index=True, comment="kind")
