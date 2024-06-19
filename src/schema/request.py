from pydantic import BaseModel


class CreateToDoRequest(BaseModel):
        #id: int
        content: str
        is_done: bool
