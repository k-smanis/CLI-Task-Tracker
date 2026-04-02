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
    created_at: datetime
    last_updated_at: datetime


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
            tasks_str = json.dumps([task.model_dump(mode="json") for task in tasks])
            f.write(tasks_str)
    except FileNotFoundError as e:
        raise FileNotFoundError("Tasks file not found") from e


def add_task(task_description: str) -> None:
    task: Task = Task(
        id=task_id_generator(),
        description=task_description,
        status=Status.NOT_STARTED,
        created_at=datetime.now(),
        last_updated_at=datetime.now(),
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


def console_print_tasks(tasks: list[Task]) -> None:
    ID_W = 4
    DESC_W = 50
    STATUS_W = 15
    CREATED_W = 26
    UPDATED_W = 26

    header = (
        f"{'ID':<{ID_W}} "
        f"{'DESCRIPTION':<{DESC_W}} "
        f"{'STATUS':<{STATUS_W}} "
        f"{'CREATED AT':<{CREATED_W}} "
        f"{'LAST UPDATED AT':<{UPDATED_W}}"
    )
    print(header)
    print("-" * len(header))

    for task in tasks:
        created_dt_formatted = task.created_at.strftime("%d %b %Y, %H:%M")
        last_updated_dt_formatted = task.last_updated_at.strftime("%d %b %Y, %H:%M")

        print(
            f"{task.id:<{ID_W}} "
            f"{task.description:<{DESC_W}} "
            f"{task.status.value:<{STATUS_W}} "
            f"{created_dt_formatted:<{CREATED_W}} "
            f"{last_updated_dt_formatted:<{UPDATED_W}}"
        )


def mark_task_in_progress(task_id: str) -> None:
    try:
        tasks = read_tasks_file()
        for task in tasks:
            if task.id == task_id:
                task.status = Status.IN_PROGRESS
                task.last_updated_at = datetime.now()
                break

        write_tasks_file(tasks)

    except FileNotFoundError as e:
        raise FileNotFoundError("Task file not found.") from e


def mark_task_done(task_id: str):
    try:
        tasks = read_tasks_file()

        for task in tasks:
            if task.id == task_id:
                task.status = Status.DONE
                task.last_updated_at = datetime.now()
                break

        write_tasks_file(tasks)

    except FileNotFoundError as e:
        raise FileNotFoundError("Task file not found.") from e


def mark_task_not_started(task_id: str):
    try:
        tasks = read_tasks_file()

        for task in tasks:
            if task.id == task_id:
                task.status = Status.NOT_STARTED
                task.last_updated_at = datetime.now()

        write_tasks_file(tasks)

    except FileNotFoundError as e:
        raise FileNotFoundError("Task file not found.") from e


def list_tasks() -> None:
    try:
        tasks: list[Task] = read_tasks_file()
        console_print_tasks(tasks)
    except FileNotFoundError as e:
        raise FileNotFoundError("Task file not found.") from e


def help():
    help_message = """
    usage: python tasker.py [ -h | --help] <command> [<args>]
    
    These are examples of the supported commands:
    
    Add new task ........................................ python tasker.py add 'read a book'
    
    Delete task (e.g. ID: 5) ............................ python tasker.py del 5
    
    List all tasks ...................................... python tasker.py ls
    
    Mark task as 'IN PROGRESS' (e.g. ID: 3) ............. python tasker.py mark-in-progress 3
    
    Mark task as 'DONE' (e.g. ID: 2) .................... python tasker.py mark-done 2
    
    Mark task as 'NOT STARTED' (e.g. ID: 1) ............. python tasker.py mark-not-started 1
    
    """
    print(help_message)


command_map: dict[str, Callable] = {
    "-h": help,
    "--help": help,
    "add": add_task,
    "del": delete_task,
    "ls": list_tasks,
    "mark-not-started": mark_task_not_started,
    "mark-in-progress": mark_task_in_progress,
    "mark-done": mark_task_done,
}

if __name__ == "__main__":
    cli_args = sys.argv[1:]
    command_name = cli_args[0]
    command_args = cli_args[1:]

    if command_name in command_map:
        command = command_map[command_name]
        command(*command_args)
    else:
        print(f"Command '{command_name}' doesn't exist.")
