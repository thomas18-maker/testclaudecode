import os
import json
import pytest
import tasks


@pytest.fixture(autouse=True)
def clean_tasks_file():
    if os.path.exists(tasks.TASKS_FILE):
        os.remove(tasks.TASKS_FILE)
    yield
    if os.path.exists(tasks.TASKS_FILE):
        os.remove(tasks.TASKS_FILE)


def test_add_task(capsys):
    tasks.add_task("Test task")
    out = capsys.readouterr().out
    assert "Added task #1" in out
    assert "[medium]" in out


def test_add_task_with_priority(capsys):
    tasks.add_task("Urgent thing", priority="high")
    out = capsys.readouterr().out
    assert "[high]" in out
    assert tasks.load_tasks()[0]["priority"] == "high"


def test_add_task_invalid_priority(capsys):
    tasks.add_task("Bad task", priority="urgent")
    assert tasks.load_tasks() == []


def test_list_shows_priority(capsys):
    tasks.add_task("Low item", priority="low")
    tasks.list_tasks()
    assert "[low]" in capsys.readouterr().out


def test_list_empty(capsys):
    tasks.list_tasks()
    assert "No tasks" in capsys.readouterr().out


def test_complete_task(capsys):
    tasks.add_task("Do something")
    tasks.complete_task(1)
    loaded = tasks.load_tasks()
    assert loaded[0]["done"] is True


def test_delete_task():
    tasks.add_task("To delete")
    tasks.delete_task(1)
    assert tasks.load_tasks() == []
