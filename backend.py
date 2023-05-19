# Reikalavimai:
# - SQLAlchemy
# - Duomenų modelio sąsajos: išnaudotas many-to-one ryšys, many-to-many būtų pliusas
# - PySimpleGUI pagrindu įgyvendinta vartotojo sąsaja
# - Išskirtas backend (modelis ir bazės sukūrimas) ir frontend (vartotojo sąsaja)
# Objektiškai realizuota vartotojo sąsaja yra didelis pliusas 


from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Table, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime, date
import os

engine = create_engine('sqlite:///db.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    # fname = Column(String)
    # lname = Column(String)
    name = Column(String)
    email = Column(String)
    # Relationships
    tasks = relationship("Task", back_populates="user")

class Priority(Base):
    __tablename__ = "priority"
    id = Column(Integer, primary_key=True)
    priority_description = Column(String)
    # Relationships
    tasks = relationship("Task", back_populates="priority")

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    status_description = Column(String)
    # Relationships
    tasks = relationship("Task", back_populates="status")

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task_description = Column(String)
    start_date = Column(String)
    finish_date = Column(String)
    priority_id = Column(Integer, ForeignKey("priority.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    # Relationships
    priority = relationship("Priority", back_populates="tasks")
    user = relationship("User", back_populates="tasks")
    status = relationship("Status", back_populates="tasks")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

