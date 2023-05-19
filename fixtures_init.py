from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import Base, Task, Priority, User, Status

engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

# Adding test data to DB

# Priority
priority = []
priority.append(Priority(priority_description='Labai žemas'))
priority.append(Priority(priority_description='Žemas'))
priority.append(Priority(priority_description='Vidutinis'))
priority.append(Priority(priority_description='Aukštas'))
priority.append(Priority(priority_description='Labai aukštas'))
session.add_all(priority)

# Users
user = []
user.append(User(name='Vardis Pavardis', email='vardis@gmail.com'))
user.append(User(name='Vardenis Pavardenis', email='vardenis@gmail.com'))
user.append(User(name='Vardė Pavardė', email='varde@gmail.com'))
user.append(User(name='Vardenė Pavardenė', email='vardene@gmail.com'))
session.add_all(user)

# Status
status = []
status.append(Status(status_description='Nepradėta'))
status.append(Status(status_description='Vykdoma'))
status.append(Status(status_description='Įvykdyta'))
status.append(Status(status_description='Atidėta'))
status.append(Status(status_description='Vėluojama'))
status.append(Status(status_description='Atšaukta'))
session.add_all(status)

# Tasks
task = []
task.append(Task(task_description='Atlikti planavimą', start_date='2023-05-16', finish_date='2023-05-30', priority_id=4, user_id=3, status_id=3))
task.append(Task(task_description='Atlikti analizę', start_date='2023-06-01', finish_date='2023-06-30', priority_id=4, user_id=3, status_id=1))
task.append(Task(task_description='Sukurti programinės įrangos architektūrą', start_date='2023-07-01', finish_date='2023-07-30', priority_id=5, user_id=2, status_id=2))
task.append(Task(task_description='Atlikti programavimo darbus', start_date='2023-08-01', finish_date='2023-08-30', priority_id=5, user_id=1, status_id=2))
task.append(Task(task_description='Atlikti programinės įrangos testavimą', start_date='2023-09-01', finish_date='2023-09-30', priority_id=3, user_id=1, status_id=2))
task.append(Task(task_description='Atlikti programinės įrangos dokumentavimą', start_date='2023-10-01', finish_date='2023-10-10', priority_id=2, user_id=1, status_id=2))
task.append(Task(task_description='Atlikti programinės įrangos diegimą', start_date='2023-10-11', finish_date='2023-10-20', priority_id=5, user_id=1, status_id=1))
task.append(Task(task_description='Atlikti programinės įrangos palaikymą ir priežiūrą', start_date='2023-10-21', finish_date='2026-12-31', priority_id=3, user_id=1, status_id=1))
session.add_all(task)

session.commit()
