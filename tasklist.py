import tkinter
from typing import List
import customtkinter as ctk
import datetime as dt
from pprint import pprint
from db import AppDB, Task


class TaskListCB(ctk.CTkScrollableFrame):
    def __init__(self, master, tasks) -> None:
        super().__init__(master)
        self.checkboxes: List = []
        self.db: AppDB = AppDB()
        self.removed: List = []
        self.show_tasks()

    def get(self) -> List:
        ''' Get a list of all the currently checked checkboxes '''
        checked_checkboxes: List = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

    def add_task(self, task) -> None:
        ''' Add's a task to the list then updates the UI to reflect. '''
        task: Task = Task(id=None, desc=task,
                    created_at=dt.datetime.utcnow(), complete=False)
        # print(task.get_task())
        self.tasks.append(task)
        self.db.create_task(task)
        self.show_tasks()

    def __CurSelect(self, event) -> None:
        ''' Helper function to select the correct checkbox. '''

        # Gets the label or canvas of the customtkinter checkbox.
        widget = event.widget

        # Now that we have the widget we clicked on
        # we need to make sure we get the lable text of the
        # widget. The customtkinter checkbox seems to be a canvas
        # and a label in a frame. So we need to make sure we get the label
        # even if we click on the canvas.
        label_txt: str = widget.master.winfo_children()[-1].cget('text')

        task: str = self.db.get_task_by_title(label_txt)
        
        match event.num:
            case 1:
                self.complete_task(task)
            case 2:
                self.remove_task(task)
            case 3:
                self.complete_task(task)


    def show_tasks(self) -> None:
        ''' Function to update the tasklist. '''
        self.checkboxes: List = []
        self.tasks: List = self.db.get_all_tasks()

        for idx, task in enumerate(self.tasks):
            if self.removed in self.tasks:
                pass
            else:
                checkbox: ctk.CTkCheckBox = ctk.CTkCheckBox(
                    self, text=task.desc, checkbox_width=15, checkbox_height=15, corner_radius=1, border_width=1)

                if task.complete:
                    checkbox.configure(state=tkinter.DISABLED)
                    checkbox.bind('<Button-3>', self.__CurSelect)
                    checkbox.bind('<Button-2>', self.__CurSelect)
                    checkbox.select()

                if checkbox._state != tkinter.DISABLED:
                    checkbox.bind('<Button-1>', self.__CurSelect)
                    checkbox.deselect()

                checkbox.grid(row=idx, column=0, padx=10, pady=(10, 0), sticky="w")
                self.checkboxes.append(checkbox)

    def complete_task(self, task: Task) -> None:
        ''' Function to mark a task completed. '''

        self.db.update_task(task)
        self.show_tasks()

    def remove_task(self, task: Task) -> None:
        ''' Remove a task '''
        self.db.remove_task(task)
        self.removed.append(task)
        print(f'Removing {task.desc}')
        self.show_tasks()
