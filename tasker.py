import sys
from typing import Callable

from pydantic import BaseModel, Field
from enum import Enum
from datetime import datetime
import os
import json


TASKS_FILE_PATH = os.path.join(os.curdir, "tasks.json")


def task_id_generator() -> str:
    """
    Generates the next available task id.

    Returns:
        str: description
    """
    if not tasks_file_exists():
        return str(1)
    else:
        with open(TASKS_FILE_PATH, "r") as f:
            tasks_str = f.read()
            tasks: list[dict] = json.loads(tasks_str)

        if len(tasks) == 0:
            return str(1)
        else:
            last_task_id = tasks[-1]["id"]
            return str(int(last_task_id) + 1)


class Status(Enum):
    NOT_STARTED = "NOT_STARTED"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"


class Task(BaseModel):
    id: str = Field(default_factory=task_id_generator)
    description: str = Field(max_length=50)
    status: Status
    created_at: str
    last_updated_at: str

    model_config = {"use_enum_values": True}


def tasks_file_exists() -> bool:
    if os.path.exists(TASKS_FILE_PATH):
        return True
    else:
        return False


def create_tasks_file() -> None:
    with open(TASKS_FILE_PATH, "w") as f:
        f.write("[]")


def read_tasks_file() -> list[Task]:
    try:
        with open(TASKS_FILE_PATH, "r") as f:
            tasks_str = f.read()
            tasks_list_of_dicts = json.loads(tasks_str)
            tasks_list = [Task(**task) for task in tasks_list_of_dicts]
            return tasks_list
    except FileNotFoundError as e:
        raise FileNotFoundError("Tasks file not found.") from e


def write_tasks_file(tasks: list[Task]) -> None:
    try:
        with open(TASKS_FILE_PATH, "w") as f:
            tasks_str = json.dumps([task.model_dump() for task in tasks])
            f.write(tasks_str)
    except FileNotFoundError as e:
        raise FileNotFoundError("Tasks file not found") from e


def add_task(task_description: str) -> None:
    task: Task = Task(
        id=task_id_generator(),
        description=task_description,
        status=Status.NOT_STARTED,
        created_at=str(datetime.now().isoformat()),
        last_updated_at=(datetime.now().isoformat()),
    )

    if not tasks_file_exists():
        create_tasks_file()

    try:
        tasks: list[Task] = read_tasks_file()
        tasks.append(task)
        write_tasks_file(tasks)
    except FileNotFoundError as e:
        raise e


def delete_task(task_id: int) -> None:
    try:
        tasks: list[Task] = read_tasks_file()
        tasks = [task for task in tasks if task.id != task_id]
        write_tasks_file(tasks)
    except FileNotFoundError as e:
        raise FileNotFoundError("Task file not found.") from e


command_map: dict[str, Callable] = {"add": add_task, "del": delete_task}

if __name__ == "__main__":
    cli_args = sys.argv[1:]
    command_name = cli_args[0]
    command_args = cli_args[1:]

    command = command_map[command_name]
    command(*command_args)
