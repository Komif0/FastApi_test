from enum import Enum
from typing import Optional, List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field


app = FastAPI(
    title="Tasks API",
    description="Simple REST API for task management",
    version="1.0.0"
)


#=============
# DTO
# =============
class TaskStatus(str, Enum):
    new = "new"
    in_progress = "in_progress"
    done = "done"

class CreateTaskDto(BaseModel):
    title: str = Field(..., min_length=1)
    description: Optional[str] = None
    status: TaskStatus

class TaskResponseDto(BaseModel):
    id: int
    title: str
    description: Optional[str]
    status: TaskStatus

#=============
# Service
#=============
class TaskService:
    def __init__(self):
        self.tasks = []
        self.next_id = 1
    def create_task(self, task_dto: CreateTaskDto):
        task = {
            "id": self.next_id,
            "title": task_dto.title,
            "description": task_dto.description,
            "status": task_dto.status
        }

        self.tasks.append(task)
        self.next_id += 1

        return task
    def get_all_tasks(self):
        return self.tasks
    def get_task_by_id(self, task_id: int):
        for task in self.tasks:
            if task["id"] == task_id:
                return task

        return None


task_service = TaskService()

# =============
# Controller
# =============
@app.post("/tasks", response_model=TaskResponseDto)
def create_task(task_dto: CreateTaskDto):
    return task_service.create_task(task_dto)

@app.get("/tasks", response_model=List[TaskResponseDto])
def get_all_tasks():
    return task_service.get_all_tasks()

@app.get("/tasks/{task_id}", response_model=TaskResponseDto)
def get_task_by_id(task_id: int):
    task = task_service.get_task_by_id(task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found"
        )
    return task