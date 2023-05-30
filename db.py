from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from typing import List
from models.tasks import Task, Base
from pprint import pprint


class AppDB:
    def __init__(self) -> None:
        self.engine = create_engine("sqlite:///tasks.db", echo=False)
        Base.metadata.create_all(bind=self.engine)
        self.Session = sessionmaker(bind=self.engine)
        self.session = self.Session()

    def create_task(self, task: Task) -> None:
        self.session.add(task)
        self.session.commit()

    def remove_task(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def update_task(self, task: Task) -> None:
        if task.complete == 1:
            task.complete = 0
            self.session.commit()
        else:
            task.complete = 1
            self.session.commit()

    def get_all_tasks(self) -> List:
        tasks = self.session.query(Task).all()
        # pprint(tasks)
        return tasks
    
    def get_task_by_title(self, task_title: str) -> Task:
        task = self.session.query(Task).where(Task.desc == task_title).first()
        return task
