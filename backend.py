# Reikalavimai:
# - SQLAlchemy
# - Duomenų modelio sąsajos: išnaudotas many-to-one ryšys, many-to-many būtų pliusas
# - PySimpleGUI pagrindu įgyvendinta vartotojo sąsaja
# - Išskirtas backend (modelis ir bazės sukūrimas) ir frontend (vartotojo sąsaja)
# Objektiškai realizuota vartotojo sąsaja yra didelis pliusas 


from sqlalchemy import Column, Integer, String, Float, ForeignKey, create_engine, Table, DATE
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
import os

engine = create_engine('sqlite:///db.db')
Base = declarative_base()


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    fname = Column(String)
    lname = Column(String)
    email = Column(String)
    # Relationships
    tasks = relationship("Task", back_populates="user")

class Priority(Base):
    __tablename__ = "priority"
    id = Column(Integer, primary_key=True)
    priority_description = Column(Integer)
    # Relationships
    tasks = relationship("Task", back_populates="priority")

class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True)
    status_description = Column(Integer)
    # Relationships
    tasks = relationship("Task", back_populates="status")

class Task(Base):
    __tablename__ = "task"
    id = Column(Integer, primary_key=True)
    task_description = Column(String)
    start_date = Column(DATE)
    finnish_date = Column(DATE)
    priority_id = Column(Integer, ForeignKey("priority.id"))
    status_id = Column(Integer, ForeignKey("status.id"))
    user_id = Column(Integer, ForeignKey("user.id"))
    # Relationships
    priority = relationship("Priority", back_populates="tasks")
    status = relationship("Status", back_populates="tasks")
    user = relationship("User", back_populates="tasks")

# class UserGroup(Base):
#     __tablename__ = "usergroup"
#     id = Column(Integer, primary_key=True)
#     user_id = Column(String)
#     team_id = Column(String)
#     # Relationships

# class team(Base):
#     __tablename__ = "team"
#     id = Column(Integer, primary_key=True)
#     team_name = Column(String)
#     # Relationships

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# Add user
def add_user(fname, lname, email):
    new_user = User(fname=fname, lname=lname, email=email)
    session.add(new_user)
    session.commit()

# Add priority
def add_priority(priority_description):
    new_description = Priority(priority_description=priority_description)
    session.add(new_description)
    session.commit

# Add status
def add_status(status_description):
    new_status = Status(status_description=status_description)
    session.add(new_status)
    session.commit


