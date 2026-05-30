import json
import os
from datetime import datetime

TASKS_FILE = "tasks.json"


def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE) as f:
        return json.load(f)


def save_tasks(tasks):
    with open(TASKS_FILE, "w") as f:
        json.dump(tasks, f, indent=2)


def add_task(title):
    tasks = load_tasks()
    task = {
        "id": len(tasks) + 1,
        "title": title,
        "done": False,
        "created": datetime.now().isoformat(),
    }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task #{task['id']}: {title}")


def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks yet.")
        return
    for t in tasks:
        status = "x" if t["done"] else " "
        print(f"[{status}] #{t['id']} {t['title']}")


def complete_task(task_id):
    tasks = load_tasks()
    for t in tasks:
        if t["id"] == task_id:
            t["done"] = True
            save_tasks(tasks)
            print(f"Completed task #{task_id}: {t['title']}")
            return
    print(f"Task #{task_id} not found.")


def delete_task(task_id):
    tasks = load_tasks()
    remaining = [t for t in tasks if t["id"] != task_id]
    if len(remaining) == len(tasks):
        print(f"Task #{task_id} not found.")
        return
    save_tasks(remaining)
    print(f"Deleted task #{task_id}.")


def main():
    import sys

    if len(sys.argv) < 2:
        print("Usage: python tasks.py <command> [args]")
        print("Commands: add <title>, list, done <id>, delete <id>")
        return

    cmd = sys.argv[1]

    if cmd == "add" and len(sys.argv) > 2:
        add_task(" ".join(sys.argv[2:]))
    elif cmd == "list":
        list_tasks()
    elif cmd == "done" and len(sys.argv) > 2:
        complete_task(int(sys.argv[2]))
    elif cmd == "delete" and len(sys.argv) > 2:
        delete_task(int(sys.argv[2]))
    else:
        print(f"Unknown command: {cmd}")


if __name__ == "__main__":
    main()
