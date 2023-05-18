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
# def add_user(fname, lname, email):
#     new_user = User(fname=fname, lname=lname, email=email)
#     session.add(new_user)
#     session.commit()

def add_user(name, email):
    new_user = User(name=name, email=email)
    session.add(new_user)
    session.commit()

# Add priority
def add_priority(priority_description):
    new_priority = Priority(priority_description=priority_description)
    session.add(new_priority)
    session.commit()

# Add status
def add_status(status_description):
    new_status = Status(status_description=status_description)
    session.add(new_status)
    session.commit()

# Add task
def add_task(task_description, start_date, finish_date, priority_id, user_id, status_id):
    new_task = Task(task_description=task_description, start_date=start_date, finish_date=finish_date, priority_id=priority_id, user_id=user_id, status_id=status_id)
    session.add(new_task)
    session.commit()

if __name__ == "__main__":
    pass
    # Adding test data to DB

    add_priority("Labai žemas")
    add_priority("Žemas")
    add_priority("Vidutinis")
    add_priority("Aukštas")
    add_priority("Labai aukštas")

    add_status("Nepradėta")
    add_status("Vykdoma")
    add_status("Įvykdyta")
    add_status("Atidėta")
    add_status("Vėluojama")
    add_status("Atšaukta")

    # add_user("Vardis", "Pavardis", "vardis@gmail.com")
    # add_user("Vardenis", "Pavardenis", "vardenis@gmail.com")
    # add_user("Vardė", "Pavardė", "varde@gmail.com")
    # add_user("Vardenė", "Pavardenė", "vardene@gmail.com")

    add_user("Vardis Pavardis", "vardis@gmail.com")
    add_user("Vardenis Pavardenis", "vardenis@gmail.com")
    add_user("Vardė Pavardė", "varde@gmail.com")
    add_user("Vardenė Pavardenė", "vardene@gmail.com")

    add_task("Atlikti planavimą", "2023-05-16", "2023-05-30", 4, 3, 3)
    add_task("Atlikti analizę", "2023-06-01", "2023-06-30", 4, 3, 1)
    add_task("Sukurti programinės įrangos architektūrą", "2023-07-01", "2023-07-30", 5, 2, 3)
    add_task("Atlikti programavimo darbus", "2023-08-01", "2023-08-30", 5, 1, 2)
    add_task("Atlikti programinės įrangos testavimą", "2023-09-01", "2023-09-30", 3, 1, 2)
    add_task("Atlikti programinės įrangos dokumentavimą", "2023-10-01", "2023-10-10", 2, 1, 2)
    add_task("Atlikti programinės įrangos diegimą", "2023-10-11", "2023-10-20", 5, 1, 1)
    add_task("Atlikti programinės įrangos palaikymą ir priežiūrą", "2023-10-21", "2026-12-31", 3, 1, 1)
