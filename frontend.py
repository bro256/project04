import PySimpleGUI as sg
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from backend import Base, User, Priority, Status, Task

# DB engine and session
# engine = create_engine('sqlite:///db.db', echo=True)
engine = create_engine('sqlite:///db.db')
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def task_list():
    tasks = session.query(Task).all()
    task_list = []
    for task in tasks:
        task_list.append([task.id, task.task_description, task.start_date, task.finish_date, 
                        task.priority.priority_description, task.user.name, task.status.status_description])
    return task_list

def update_task_list():
    tasks = session.query(Task).all()
    task_list = []
    for task in tasks:
        task_list.append([task.id, task.task_description, task.start_date, task.finish_date,
                          task.priority.priority_description, task.user.name, task.status.status_description])
    print(f'TASK DATA: {task_list}')
    window['-TABLE-'].update(values=task_list)

task_list = task_list()

# Dropdown menu
priority_list = [priority.priority_description for priority in session.query(Priority).all()]
status_list = [status.status_description for status in session.query(Status).all()]
user_list = [user.name for user in session.query(User).all()]

# GUI theme
sg.theme('LightGrey1')

##################################### Main Window #################################
# Main window layout
layout = [
    [sg.Table(values=task_list, key='-TABLE-',
              headings=['ID', 'Description', 'Start Date', 'Finish Date', 'Priority', 'Assignee', 'Status'],
              display_row_numbers=True,
              auto_size_columns=True,
              justification='left',
              num_rows=min(20, len(task_list)))],
    [sg.Button('Add Task'), sg.Button('Edit Task'), sg.Button('Delete Task'), sg.Button('Exit')],
]

window = sg.Window('Task Management', layout)

# Main window events
while True:
    event, values = window.read()
    print(f'VALUES: {values}')
    if event == sg.WINDOW_CLOSED or event == 'Exit':
        break

##################################### Add Task #################################
    if event == 'Add Task':
        # Add task layout
        add_layout = [
            [sg.Text('Task Description:'), sg.InputText(key='-DESCRIPTION-')],
            [sg.Text('Start Date:'), sg.InputText(key='-STARTDATE-')],
            [sg.Text('Finish Date:'), sg.InputText(key='-FINISHDATE-')],
            # [sg.Text('Priority:'), sg.InputText(key='-PRIORITY-')],
            [sg.Text("Priority:")], [sg.Combo(priority_list, key="-PRIORITY-")],
            # [sg.Text('Assignee:'), sg.InputText(key='-ASSIGNEE-')],
            [sg.Text("Asignee:")], [sg.Combo(user_list, key="-ASSIGNEE-")],    
            # [sg.Text('Status:'), sg.InputText(key='-STATUS-')],
            [sg.Text("Status:")], [sg.Combo(status_list, key="-STATUS-")],
            [sg.Button('Add'), sg.Button('Cancel')],
        ]

        # Add task window
        add_window = sg.Window('Add Task', add_layout)
        while True:
            add_event, add_values = add_window.read()
            if add_event == sg.WINDOW_CLOSED or add_event == 'Cancel':
                break
            if add_event == 'Add':
                task = Task(
                    task_description=add_values['-DESCRIPTION-'],
                    start_date=add_values['-STARTDATE-'],
                    finish_date=add_values['-FINISHDATE-'],
                )

                # Select/add PRIORITY
                priority_description = add_values['-PRIORITY-']
                priority = session.query(Priority).filter_by(priority_description=priority_description).first()
                if not priority:
                    priority = Priority(priority_description=priority_description)
                task.priority = priority

                # Select/add USER
                name = add_values['-ASSIGNEE-']
                user = session.query(User).filter_by(name=name).first()
                if not user:
                    user = User(name=name)
                task.user = user

                # Select/add STATUS
                status_description = add_values['-STATUS-']
                status = session.query(Status).filter_by(status_description=status_description).first()
                if not status:
                    status = Status(status_description=status_description)
                task.status = status

                session.add(task)
                session.commit()

                sg.popup('Task added successfully!')
                add_window.close()
                update_task_list()
        add_window.close()

##################################### Edit Task #################################

    if event == ('Edit Task'):
        selected_rows = values['-TABLE-']
        print(f'SELECTED ROWS: {selected_rows}')
        if len(selected_rows) != 1:
            sg.popup("Select one task")
        else:
            selected_task_id = int(task_list[selected_rows[0]][0])
            print(f'SELECTED_TASK_ID: {selected_task_id}')
            selected_task = session.query(Task).get(selected_task_id)
            print(f'SELECTED_TASK: {selected_task}')

            # Edit task layout
            priority_list = [priority.priority_description for priority in session.query(Priority).all()]
            edit_layout = [
                [sg.Text('Task Description:'), sg.InputText(selected_task.task_description, key='-DESCRIPTION-')],
                [sg.Text('Start Date:'), sg.InputText(selected_task.start_date, key='-STARTDATE-')],
                [sg.Text('Finish Date:'), sg.InputText(selected_task.finish_date, key='-FINISHDATE-')],
                # [sg.Text('Priority:'), sg.InputText(selected_task.priority.priority_description, key='-PRIORITY-')],
                [sg.Text("Priority:")], [sg.Combo(priority_list, key="-PRIORITY-")],
                # [sg.Text('Assignee:'), sg.InputText(selected_task.user.name, key='-ASSIGNEE-')],
                [sg.Text("Asignee:")], [sg.Combo(user_list, key="-ASSIGNEE-")],              
                #[sg.Text('Status:'), sg.InputText(selected_task.status.status_description, key='-STATUS-')],
                [sg.Text("Status:")], [sg.Combo(status_list, key="-STATUS-")],
                [sg.Button('Update Task'), sg.Button('Cancel')],
            ]

            # Edit task window
            edit_window = sg.Window('Edit Task', edit_layout)
            while True:
                edit_event, edit_values = edit_window.read()
                if edit_event == sg.WINDOW_CLOSED or edit_event == 'Cancel':
                    break
                if edit_event == 'Update Task':
                    selected_task.task_description = edit_values['-DESCRIPTION-']
                    selected_task.start_date = edit_values['-STARTDATE-']
                    selected_task.finish_date = edit_values['-FINISHDATE-']

                    # Update PRIORITY
                    priority_description = edit_values['-PRIORITY-']
                    priority = session.query(Priority).filter_by(priority_description=priority_description).first()
                    if priority:
                        selected_task.priority = priority

                    # Update ASSIGNEE
                    assignee_name = edit_values['-ASSIGNEE-']
                    assignee = session.query(User).filter_by(name=assignee_name).first()
                    if assignee:
                        selected_task.user = assignee

                    # Update STATUS
                    status_description = edit_values['-STATUS-']
                    status = session.query(Status).filter_by(status_description=status_description).first()
                    if status:
                        selected_task.status = status

                    session.commit()
                    sg.popup('Task updated successfully!')
                    edit_window.close()

            update_task_list()
            edit_window.close()


##################################### Delete Task #################################

    if event == 'Delete Task':
        selected_rows = values['-TABLE-']
        print(f'SELECTED ROWS: {selected_rows}')
        if len(selected_rows) != 1:
            sg.popup('Select one task to delete.')
        else:
            selected_task_id = int(task_list[selected_rows[0]][0])
            print(f'SELECTED_TASK_ID: {selected_task_id}')
            selected_task = session.query(Task).get(selected_task_id)
            print(f'SELECTED_TASK: {selected_task}')

            confirm_msg = 'Are you sure you want to delete the selected task?'
            confirm_dialog = sg.popup_yes_no(confirm_msg, title='Confirm Deletion')
            if confirm_dialog == 'Yes':
                session.delete(selected_task)
                session.commit()
                sg.popup('Task(s) deleted successfully!')
                update_task_list()

# Close
session.close()
window.close()

