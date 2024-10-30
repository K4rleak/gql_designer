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

class GQLInterfaceModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "interfaces"

    name = Column(String, comment="name of the type")
    description = Column(String, comment="description of the type")
    isDeprecated = Column(Boolean, comment="if it is depreacted", default=False)
    deprecationReason = Column(String, comment="the reason why it is deprecated", nullable=True)

