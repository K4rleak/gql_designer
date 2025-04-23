# models/type_model.py

import sqlalchemy
from sqlalchemy import Column, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from .Base import BaseModel

class TemplateModel(BaseModel):
    __tablename__ = "templates"

    name = Column(String, comment="name of the type")
