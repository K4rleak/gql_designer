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

class GQLFieldModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "fields"


    name = Column(String, comment="name of the group")
    description = Column(String, comment="description of the group")
    isDeprecated = Column(Boolean, comment="if it is depreacted", default=False)
    deprecationReason = Column(String, comment="the reason why it is deprecated", nullable=True)
    master_type_id = Column(ForeignKey('types.id'), index=True, comment="type which owns this field")


    typeof_id = Column(ForeignKey("types.id"), index=True, comment="type of this field")
    #co to je za typ fieldu
   
    typeof = relationship("GQLTypeModel", viewonly=True)
