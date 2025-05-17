import sqlalchemy
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from .Base import BaseModel

class FacilityGQLModel(BaseModel):
    """Entity representing a Facility"""

    __tablename__ = "facilitygqlmodels"

#krome id vse muze byt nullable, id nemusi byt
    id = Column(String, nullable=, comment="Entity primary key")
    name = Column(String, nullable=, comment="Name ")
    nameEn = Column(String, nullable=, comment="English name")
    lastchange = Column(DateTime, nullable=, comment="Time of last update")
    created = Column(DateTime, nullable=, comment="Time of entity introduction")
    label = Column(String, nullable=, comment="Facility full name assigned by an administrator")
    address = Column(String, nullable=, comment="Facility address")
    valid = Column(Boolean, nullable=, comment="is the facility still valid")
    capacity = Column(Integer, nullable=, comment="Facility's capacity")
    geometry = Column(String, nullable=, comment="Facility geometry (SVG)")
    geolocation = Column(String, nullable=, comment="Facility geo address (WGS84+zoom)")
    changedby = Column(String, ForeignKey('usergqlmodels.id'), nullable=, comment="Who made last change")
    reservations = Column(String, nullable=, comment="Intermediate entity linking the event and facility")
    externalIds = Column(String, nullable=, comment="All related external ids")
    group = Column(String, ForeignKey('groups.id'), nullable=, comment="Facility management group")
    plannedLessons = Column(String, ForeignKey('plannedlessongqlmodels.id'), nullable=, comment="planned items")