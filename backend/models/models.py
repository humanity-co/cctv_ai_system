from sqlalchemy import Column, Integer, String, Float, DateTime, JSON, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
import datetime

Base = declarative_base()

class Camera(Base):
    __tablename__ = "cameras"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    source_url = Column(String)
    location = Column(String)
    status = Column(String, default="active")

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True)
    type = Column(String) # intrusion, crowd_alert, unknown_person, fire, accident
    message = Column(String)
    confidence = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    snapshot_path = Column(String)
    camera_id = Column(Integer, ForeignKey("cameras.id"))
    metadata_json = Column(JSON) # Store additional context

class Person(Base):
    __tablename__ = "persons"
    id = Column(Integer, primary_key=True)
    name = Column(String)
    embedding = Column(JSON) # To be moved to FAISS for production
    is_known = Column(Integer, default=1)
