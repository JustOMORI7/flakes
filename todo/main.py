#!/usr/bin/env python3
import json
import os
import sys

FILE = os.path.expanduser("~/.todos.json")

def load_todos():
    if os.path.exists(FILE):
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

def save_todos(todos):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(todos, f, indent=2, ensure_ascii=False)

def add_task(task):
    todos = load_todos()
    todos.append({"task": task, "done": False})
    save_todos(todos)
    print(f"Task added: {task}")

def list_tasks():
    todos = load_todos()
    if not todos:
        print("No tasks yet.")
        return
    for i, t in enumerate(todos, 1):
        status = "x" if t["done"] else " "
        print(f"{i}. [{status}] {t['task']}")

def mark_done(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        todos[index]["done"] = True
        save_todos(todos)
        print(f"Task completed: {todos[index]['task']}")
    else:
        print("Invalid task number.")

def delete_task(index):
    todos = load_todos()
    if 0 <= index < len(todos):
        removed = todos.pop(index)
        save_todos(todos)
        print(f"Deleted: {removed['task']}")
    else:
        print("Invalid task number.")

def help_menu():
    print("""
Usage:
  todo add "Task"      → Add new task
  todo list            → List tasks
  todo done 2          → Complete the second task
  todo del 3           → Delete the third task
""")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        help_menu()
    else:
        cmd = sys.argv[1]
        if cmd == "add":
            add_task(" ".join(sys.argv[2:]))
        elif cmd == "list":
            list_tasks()
        elif cmd == "done":
            if len(sys.argv) > 2 and sys.argv[2].isdigit():
                mark_done(int(sys.argv[2]) - 1)
            else:
                print("Enter valid task number.")
        elif cmd == "del":
            if len(sys.argv) > 2 and sys.argv[2].isdigit():
                delete_task(int(sys.argv[2]) - 1)
            else:
                print("Enter valid task number.")
        else:
            help_menu()
