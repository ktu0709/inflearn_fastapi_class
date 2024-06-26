from fastapi import FastAPI , Body , HTTPException , Depends
from pydantic import BaseModel

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
def get_todos_handler(order:str | None = None,):
        ret = list(todo_data.values())
        if order == "DESC":
                return ret[::-1]
        return ret


# 단일 조회
@app.get("/todos/{todo_id}", status_code= 200)
def get_todo_handler(todo_id: int):
        return todo_data.get(todo_id,{})

#삽입
class CreateToDoRequest(BaseModel):
        id: int
        content: str
        is_done: bool

@app.post("/todos", status_code= 201)
def create_todo_handler(request: CreateToDoRequest):
        todo_data[request.id] = request.dict()
        return todo_data[request.id]

#수정
@app.patch("/todos/{todo_id}", status_code= 200)
def update_todo_handler(
        todo_id:int,
        content : str = Body(..., embed=True),
        is_done : bool = Body(..., embed=True),
    ):
        todo = todo_data.get(todo_id)
        if todo:
                todo["content"] = content
                todo["is_done"] = is_done
                return todo
        raise HTTPException(status_code=404,detail="ToDo Not Found")

#삭제
@app.delete("/todos/{todo_id}", status_code= 204)
def delete_todo_handler(todo_id : int):
        todo = todo_data.pop(todo_id,None)
        if todo:
                return
        raise HTTPException(status_code=404,detail="ToDo Not Found")