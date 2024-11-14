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

class GQLPossibleTypeRelationModel(BaseModel):
    """Spravuje mozne typy spojene s typem"""

    __tablename__ = "possible_types_association"

    type_id = Column(ForeignKey('types.id'), primary_key=True)
    possible_type_id = Column(ForeignKey('types.id'), primary_key=True)
 

