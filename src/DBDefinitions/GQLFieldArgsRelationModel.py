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

class GQLFieldArgsRelationModel(BaseModel):
    """Spravuje mozne typy spojene s typem"""

    
    __tablename__ = "field_args_association"
    field_id = Column(ForeignKey('fields.id'), primary_key=True)
    arg_id = Column(ForeignKey('args.id'), primary_key=True)
 

