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

class GQLTypeInterfaceRelationModel(BaseModel):
    """Spravuje data spojena se skupinou"""

    __tablename__ = "type_interface_association"

    type_id = Column(ForeignKey('types.id'), primary_key=True)
    interface_id = Column(ForeignKey('interfaces.id'), primary_key=True)
    #trrr = Column(ForeignKey('types.id'), primary_key=True),

    #trrr = Column(ForeignKey('interfaces.id'), primary_key=True)

