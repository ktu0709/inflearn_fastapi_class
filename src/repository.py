from sqlalchemy.orm import Session
from sqlalchemy import select ,delete
from orm import ToDo
from typing import List
def get_todos(session:Session) -> List[ToDo]:
        return list(session.scalars(select(ToDo)))

def get_todo_by_todo_id(session : Session,todo_id : int) -> ToDo | None:
        return session.scalar(select(ToDo).where(ToDo.id==todo_id))

def create_todo(session : Session,todo:ToDo) -> ToDo:
        session.add(instance=todo)
        session.commit() # db insert
        session.refresh(instance=todo)
        return todo

def update_todo(session : Session,todo:ToDo) -> ToDo:
        session.add(instance=todo)
        session.commit() # db insert
        session.refresh(instance=todo)
        return todo

def delete_todo(session : Session,todo_id : int) -> None:
        session.execute(delete(ToDo).where(ToDo.id == todo_id))
        session.commit()