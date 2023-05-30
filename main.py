import tkinter
from typing import Optional, Tuple, Union, List
from datetime import datetime
import customtkinter as ctk
from tasklist import TaskListCB
from db import AppDB
from pprint import pprint

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")


class AppFrame(ctk.CTkFrame):

    def __init__(self, master, **kwargs) -> None:
        ''' Setup a frame in our app that will hold all the other widgets '''
        super().__init__(master, **kwargs)
        self.db: AppDB = AppDB()
        self.tasks: List = self.db.get_all_tasks()

        # Add widgets to frame.
        self.lbl_txt_entry: ctk.CTkLabel = ctk.CTkLabel(master=self, text='Enter task.')
        self.lbl_txt_entry.grid(row=1, column=0)

        self.txt_entry: ctk.CTkEntry = ctk.CTkEntry(master=self)
        self.txt_entry.grid(row=2, column=0, pady=10)

        self.button: ctk.CTkButton = ctk.CTkButton(
            master=self, text="Add Task", command=self.add_task_btn_pressed)
        self.button.grid(row=3, column=0, pady=10)

        self.tasklist: TaskListCB = TaskListCB(self, tasks=self.tasks)
        # Fix for customtkinter scrollable frame mouse wheel scrolling. Doesn't work in linux without these two lines of code
        # Havent tested in windows to make sure it still works in windows.
        # https://github.com/TomSchimansky/CustomTkinter/issues/1356
        self.tasklist.bind_all("<Button-4>", lambda e: self.tasklist._parent_canvas.yview("scroll", -1, "units"))
        self.tasklist.bind_all("<Button-5>", lambda e: self.tasklist._parent_canvas.yview("scroll", 1, "units"))

        self.tasklist.grid(row=4, column=0, sticky="nsew", padx=20, pady=10)

    def add_task_btn_pressed(self) -> None:
        ''' This is a callback for the button on the form.
            When this button is clicked it add's a task to the list. '''
        task: str = self.txt_entry.get()
        self.txt_entry.delete(first_index=0, last_index=255)
        self.tasklist.add_task(task)


class App(ctk.CTk):

    def __init__(self) -> None:
        super().__init__()

        self.geometry("300x400")
        self.title("Todo App")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.myframe: AppFrame = AppFrame(master=self)
        self.myframe.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")


if __name__ == "__main__":
    app: App = App()
    app.mainloop()
