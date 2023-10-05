import tkinter as tk
from tkinter import ttk, simpledialog, messagebox, Toplevel
from tkcalendar import Calendar
import sqlite3
from datetime import datetime


class TaskOrganizer(tk.Tk):

    def __init__(self):
        super().__init__()

        # Try to connect to database
        try:
            self.conn = sqlite3.connect('tasks.db')
            self.cursor = self.conn.cursor()
            self.create_table()
        except Exception as e:
            print(f"Database Error: {e}")
            return

        self.tasks = self.load_tasks_from_db()

        self.title('Task Organizer')
        self.geometry('500x600')
        self.configure(bg='#2c3e50')

        self.style = ttk.Style(self)
        self.style.configure('TButton',
                             font=('Arial', 12),
                             background='#3498db',
                             foreground='black',
                             borderwidth=1,
                             relief="solid")
        self.style.map('TButton',
                       background=[('active', '#2980b9')])
        self.style.configure('TLabel',
                             font=('Arial', 14),
                             padding=10,
                             background='#2c3e50',
                             foreground='white')

        self.label = ttk.Label(self, text="Your Tasks")
        self.label.pack(pady=20)

        self.task_listbox = tk.Listbox(self, font=('Arial', 12), width=50, bg='#ecf0f1', relief="solid", bd=1)
        self.task_listbox.pack(pady=10, padx=20)
        self.task_listbox.bind('<Double-Button-1>', self.show_task_details)

        self.button_frame = ttk.Frame(self)
        self.button_frame.pack(pady=20, padx=20)

        self.add_button = ttk.Button(self.button_frame, text='Add Task', command=self.add_task)
        self.add_button.grid(row=0, column=0, padx=10)

        self.edit_button = ttk.Button(self.button_frame, text='Edit Task', command=self.edit_task)
        self.edit_button.grid(row=0, column=1, padx=10)

        self.delete_button = ttk.Button(self.button_frame, text='Delete Task', command=self.delete_task)
        self.delete_button.grid(row=0, column=2, padx=10)

        # Przyciski do zmiany statusu zadania
        self.mark_completed_button = ttk.Button(self.button_frame, text='Mark Completed', command=self.mark_completed)
        self.mark_completed_button.grid(row=1, column=0, padx=10)

        self.mark_working_button = ttk.Button(self.button_frame, text='Mark Still Working', command=self.mark_still_working)
        self.mark_working_button.grid(row=1, column=1, padx=10)

        self.clock_label = ttk.Label(self, text="", background='#2c3e50', foreground='white')
        self.clock_label.pack(pady=5)
        self.update_clock()

        self.complete_label = ttk.Label(self, text="", background='#2c3e50', foreground='white')
        self.complete_label.pack(pady=5)
        self.update_completion_label()

        self.protocol("WM_DELETE_WINDOW", self.on_closing)

    def create_table(self):
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS tasks 
                                (id INTEGER PRIMARY KEY, 
                                task TEXT NOT NULL, 
                                description TEXT, 
                                deadline DATE, 
                                status TEXT NOT NULL DEFAULT "still_working")''')
        self.conn.commit()

    def load_tasks_from_db(self):
        self.cursor.execute("SELECT task, status FROM tasks")
        tasks_in_db = self.cursor.fetchall()
        return tasks_in_db

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task:")
        description = simpledialog.askstring("Add Task", "Enter description for the task:")

        cal = Calendar(self, selectmode='day', year=2023, month=10, day=5)
        cal.pack(pady=20, padx=20)
        cal_date = cal.selection_get()
        self.conn.execute("INSERT INTO tasks (task, description, deadline) VALUES (?, ?, ?)", (task, description, cal_date))
        self.conn.commit()
        self.tasks.append((task, "still_working"))
        self.update_listbox()
        cal.pack_forget()

    def edit_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, _ = self.tasks[selected_index[0]]
            new_task = simpledialog.askstring("Edit Task", "Edit task:", initialvalue=task)
            if new_task:
                self.tasks[selected_index[0]] = (new_task, "still_working")
                self.update_listbox()

    def delete_task(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            self.conn.execute("DELETE FROM tasks WHERE task=?", (self.tasks[selected_index[0]][0],))
            self.conn.commit()
            del self.tasks[selected_index[0]]
            self.update_listbox()

    def update_listbox(self):
        self.task_listbox.delete(0, tk.END)
        for task, status in self.tasks:
            if status == "completed":
                self.task_listbox.insert(tk.END, task)
                self.task_listbox.itemconfig(tk.END, {'bg': 'green'})
            else:
                self.task_listbox.insert(tk.END, task)
                self.task_listbox.itemconfig(tk.END, {'bg': 'yellow'})

    def update_clock(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.after(1000, self.update_clock)

    def update_completion_label(self):
        completed = sum(1 for _, status in self.tasks if status == "completed")
        total = len(self.tasks)
        self.complete_label.config(text=f"Complete tasks: {completed}/{total}")

    def mark_completed(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, _ = self.tasks[selected_index[0]]
            self.conn.execute("UPDATE tasks SET status='completed' WHERE task=?", (task,))
            self.conn.commit()
            self.tasks = self.load_tasks_from_db()
            self.update_listbox()
            self.update_completion_label()

    def mark_still_working(self):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, _ = self.tasks[selected_index[0]]
            self.conn.execute("UPDATE tasks SET status='still_working' WHERE task=?", (task,))
            self.conn.commit()
            self.tasks = self.load_tasks_from_db()
            self.update_listbox()
            self.update_completion_label()

    def show_task_details(self, event):
        selected_index = self.task_listbox.curselection()
        if selected_index:
            task, _ = self.tasks[selected_index[0]]
            self.cursor.execute("SELECT description FROM tasks WHERE task=?", (task,))
            description = self.cursor.fetchone()[0]
            messagebox.showinfo("Task Details", f"Task: {task}\n\nDescription: {description}")

    def on_closing(self):
        self.conn.close()
        self.destroy()


def add_missing_columns(self):
    # Check if the status column exists
    self.cursor.execute("PRAGMA table_info(tasks)")
    columns = self.cursor.fetchall()
    column_names = [column[1] for column in columns]

    if "status" not in column_names:
        self.cursor.execute("ALTER TABLE tasks ADD COLUMN status TEXT DEFAULT 'still_working'")
        self.conn.commit()
        
def update_completion_label(self):
    completed = sum(1 for _, status in self.tasks if status == "completed")
    total = len(self.tasks)
    self.complete_label.config(text=f"Complete tasks: {completed}/{total}")

if __name__ == "__main__":
    try:
        app = TaskOrganizer()
        app.mainloop()
    except Exception as e:
        print(f"Error: {e}")
