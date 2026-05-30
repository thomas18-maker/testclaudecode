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
