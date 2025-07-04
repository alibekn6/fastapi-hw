from pydantic import BaseModel


class TaskCreateSchema(BaseModel):
    title: str
    description: str


class TaskGetSchema(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        from_attributes = True
