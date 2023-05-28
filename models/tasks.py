from typing import Any, List, Optional
from sqlalchemy import ForeignKey, String, DateTime, Integer, Column, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.functions import now
import datetime as dt

Base = declarative_base()


class Task(Base):
    __tablename__ = "tasks"

    id = Column('id', Integer, primary_key=True, autoincrement=True)
    desc = Column('desc', String(45))
    created_at = Column(DateTime, default=now)
    complete = Column(Boolean, default=False)

    def __init__(self, id, desc, created_at, complete):
        self.id = id
        self.desc = desc
        self.created_at = created_at
        self.complete = complete

    def __repr__(self):
        return f"({self.id}) {self.desc} - {self.created_at} - {self.complete}"

    def get_task(self):
        return {
            'id': self.id,
            'desc': self.desc,
            'created_at': self.created_at,
            'completed_at': self.complete
        }
