import tkinter
import customtkinter as ctk
import datetime as dt
from pprint import pprint
from db import AppDB, Task


class TaskListCB(ctk.CTkScrollableFrame):
    def __init__(self, master, tasks):
        super().__init__(master)
        self.checkboxes = []
        self.db = AppDB()
        self.tasks = self.db.get_all_tasks()
        # self.bind('')

        self.show_tasks()

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

    def add_task(self, task):
        ''' Add's a task to the list then updates the UI to reflect. '''
        task = Task(id=None, desc=task,
                    created_at=dt.datetime.utcnow(), complete=False)
        # print(task.get_task())
        self.tasks.append(task)
        self.db.create_task(task)
        self.show_tasks()

    def __CurSelect(self, event):
        ''' Helper function to select the correct checkbox. '''

        # Gets the label or canvas of the customtkinter checkbox.
        widget = event.widget

        # I don't even know how to describe this...
        # Now that we have the widget we clicked on
        # we need to make sure we get the lable text of the
        # widget. The customtkinter checkbox seems to be a canvas
        # and a label in a frame. So we need to make sure we get the label
        # even if we click on the canvas.
        label_txt = widget.master.winfo_children()[-1].cget('text')
        try:
            task = self.db.get_task_by_title(label_txt)
            self.complete_task(task, widget.master)
        except:
            pass

    def show_tasks(self):
        ''' Function to update the tasklist. '''
        for idx, task in enumerate(self.tasks):
            checkbox = ctk.CTkCheckBox(
                self, text=task.desc, checkbox_width=15, checkbox_height=15, corner_radius=1, border_width=1)

            if task.complete:
                checkbox.configure(state=tkinter.DISABLED)
                checkbox.bind('<Button-3>', self.__CurSelect)
                checkbox.select()

            if checkbox._state != tkinter.DISABLED:
                checkbox.bind('<Button-1>', self.__CurSelect)
                checkbox.deselect()

            checkbox.grid(row=idx, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def complete_task(self, task: Task, chkbox_widget: ctk.CTkCheckBox) -> None:
        ''' Function to mark a task completed. '''

        updated_task = self.db.update_task(task.id)
        # now make sure we can't click on it again.
        # if updated_task.complete:
        #     # Configure the checkbox widget to be disabled after completing.
        #     chkbox_widget.configure(state=tkinter.DISABLED)
        #     chkbox_widget.unbind('<Button-1>')
        #     chkbox_widget.bind('<Button-3>', self.__CurSelect)
            
        self.show_tasks()
