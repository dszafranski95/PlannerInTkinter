# Task Organizer

A simple desktop application to manage tasks using Python's tkinter library and sqlite3 for database management.

## Features
1. List down your tasks with a deadline.
2. Mark tasks as completed.
3. Double click on a task to see its details.
4. Edit or delete tasks.
5. Dynamic clock display.
6. Task completion statistics.

## Prerequisites
1. Python 3.x
2. sqlite3 (included in Python standard library)
3. tkinter (included in Python standard library)
4. tkcalendar (`pip install tkcalendar`)

## Usage
1. Ensure all prerequisites are installed.
2. Run the script: `python <filename>.py`

## Structure
* `TaskOrganizer`: The main class which provides the GUI and interacts with the database.
  - `create_table`: Initializes the database table.
  - `load_tasks_from_db`: Fetches tasks from the database.
  - `add_task`: Adds a new task.
  - `edit_task`: Edits an existing task.
  - `delete_task`: Deletes a task.
  - `update_listbox`: Updates the display list of tasks.
  - `update_clock`: Updates the clock in real-time.
  - `update_completion_label`: Updates the task completion statistics.
  - `mark_completed`: Marks a task as completed.
  - `mark_still_working`: Marks a task as still in progress.
  - `show_task_details`: Displays task details on double click.
  - `on_closing`: Closes the database connection on app closure.
  
* `add_missing_columns`: Function to add missing columns in the database.
  
* `update_completion_label`: Function to update the completion label.

## Issues
If you encounter any issues or have feature suggestions, please open an issue or submit a pull request.

## License
This project is open-source. Feel free to use, modify, and distribute the code.

