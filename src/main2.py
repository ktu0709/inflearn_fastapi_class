from typing import List

from fastapi import FastAPI , Body , HTTPException , Depends
from sqlalchemy.orm import Session
from connection import get_db
from orm import ToDo
from repository import get_todos, get_todo_by_todo_id, create_todo, update_todo, delete_todo
from schema.request import CreateToDoRequest
from schema.response import ToDoListSchema, ToDoSchema

app = FastAPI()

@app.get("/" , status_code= 200)
def health_check_handler():
        return{"ping":"pong"}

todo_data = {
        1:{
           "id":1,
           "content" : "실전! FastAPI 섹션 0 수강",
           "is_done" : True,
        },
        2: {
                "id": 2,
                "content": "실전! FastAPI 섹션 1 수강",
                "is_done": False,
        },
        3: {
                "id": 3,
                "content": "실전! FastAPI 섹션 2 수강",
                "is_done": False,
        }
}
# 전체 조회
@app.get("/todos", status_code= 200)
def get_todos_handler(order:str | None = None,
                      session:Session=Depends(get_db),
                      ):
        todos: List[ToDo] = get_todos(session=session)


        if order == "DESC":
                return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos[::-1]]
        )
        return ToDoListSchema(
            todos=[ToDoSchema.from_orm(todo) for todo in todos]
        )


# 단일 조회
@app.get("/todos/{todo_id}", status_code= 200)
def get_todo_handler(todo_id: int,session:Session=Depends(get_db),) -> ToDoSchema:
        todo : ToDo | None = get_todo_by_todo_id(session=session,todo_id = todo_id)
        if todo:
            return ToDoSchema.from_orm(todo)
        return HTTPException(status_code=404,detail="ToDo Not Found")

#삽입

@app.post("/todos", status_code= 201)
def create_todo_handler(request: CreateToDoRequest,session:Session=Depends(get_db)) -> ToDoSchema:
        todo : ToDo = ToDo.create(request=request)
        todo : ToDo = create_todo(session=session , todo=todo)
        return ToDoSchema.from_orm(todo)

#수정
@app.patch("/todos/{todo_id}", status_code= 200)
def update_todo_handler(
        todo_id:int,
        content : str = Body(..., embed=True),
        is_done : bool = Body(..., embed=True),
        session:Session=Depends(get_db)
    ):
        todo : ToDo | None = get_todo_by_todo_id(session=session,todo_id = todo_id)
        if todo:
               todo.done() if is_done else todo.undone()
               todo : ToDo = update_todo(session=session,todo=todo)
               return ToDoSchema.from_orm(todo)
        raise HTTPException(status_code=404,detail="ToDo Not Found")

#삭제
@app.delete("/todos/{todo_id}", status_code= 204)
def delete_todo_handler(todo_id : int , session:Session=Depends(get_db)):
        todo: ToDo | None = get_todo_by_todo_id(session=session, todo_id=todo_id)
        if not todo:
                raise HTTPException(status_code=404, detail="ToDo Not Found")

        delete_todo(session=session,todo_id=todo_id)
