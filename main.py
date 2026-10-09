import json
import shutil

STATUS_ICONS = {True: "[X]", False: "[ ]"}

TASKS_FILE = "tasks.json"


class TaskNotFoundError(Exception):
    pass


class TaskAlreadyCompletedError(Exception):
    pass


class EmptyTaskError(Exception):
    pass


def add_task(tasks, name):
    if not name.strip():
        raise EmptyTaskError("The task name cannot be empty.")
    task = {
        "name": name.strip(),
        "completed": False
    }
    tasks.append(task)


def list_tasks(tasks):
    print("\nTask list:")
    if not tasks:
        print("There are no tasks in the list.")
        return
    for i, task in enumerate(tasks, start=1):
        status = STATUS_ICONS[task["completed"]]
        print(f"{i}. {task['name']} - {status}")


def complete_task(tasks, number):
    if number < 1 or number > len(tasks):
        raise TaskNotFoundError(number)
    if tasks[number - 1]["completed"]:
        raise TaskAlreadyCompletedError(number)
    tasks[number - 1]["completed"] = True


def save_tasks(tasks, path):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=4)


def load_tasks(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        shutil.copy(path, path + ".bak")
        print(f"Error: The tasks file is corrupted. A copy was saved as {path}.bak and a new empty list will be used.")
        return []
    except FileNotFoundError:
        return []


def delete_task(tasks, number):
    if number < 1 or number > len(tasks):
        raise TaskNotFoundError(number)
    return tasks.pop(number - 1)


def confirm(question):
    while True:
        answer = input(f"{question} (Y/N): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"


def edit_task(tasks, number, new_name):
    if number < 1 or number > len(tasks):
        raise TaskNotFoundError(number)
    if not new_name.strip():
        raise EmptyTaskError("The new name cannot be empty.")
    tasks[number - 1]["name"] = new_name.strip()


def main():
    tasks = load_tasks(TASKS_FILE)

    while True:
        print("\nOptions:")
        print("1. Add task")
        print("2. List tasks")
        print("3. Complete task")
        print("4. Delete task")
        print("5. Edit task")
        print("6. Exit")

        option = input("Select an option: ").strip()

        if option == "1":
            task_name = input("Enter the task name: ").strip()
            try:
                add_task(tasks, task_name)
                save_tasks(tasks, TASKS_FILE)
                print(f"Task '{task_name}' added.")
            except EmptyTaskError as e:
                print(f"Error: {e} Try again.")
        elif option == "2":
            list_tasks(tasks)
        elif option == "3":
            try:
                task_number = int(input("Enter the number of the task to complete: "))
                complete_task(tasks, task_number)
                save_tasks(tasks, TASKS_FILE)
                name = tasks[task_number - 1]["name"]
                print(f"Task number {task_number}. {name} completed.")
            except ValueError:
                print("Error: You must enter a valid number.")
            except TaskNotFoundError as e:
                print(f"Error: task {e} does not exist.")
            except TaskAlreadyCompletedError as e:
                print(f"Error: task {e} is already completed.")
        elif option == "4":
            try:
                task_number = int(input("Enter the number of the task to delete: "))
                if task_number < 1 or task_number > len(tasks):
                    raise TaskNotFoundError(task_number)
                if confirm("Are you sure you want to delete this task?"):
                    deleted = delete_task(tasks, task_number)
                    save_tasks(tasks, TASKS_FILE)
                    print(f"Task {task_number}. {deleted['name']} deleted.")
                else:
                    print("Deletion cancelled.")
            except ValueError:
                print("Error: You must enter a valid number.")
            except TaskNotFoundError as e:
                print(f"Error: task {e} does not exist.")
        elif option == "5":
            try:
                task_number = int(input("Enter the task number: "))
                if task_number < 1 or task_number > len(tasks):
                    raise TaskNotFoundError(task_number)
                new_task_name = input("Enter the new task name: ").strip()
                old_name = tasks[task_number - 1]["name"]
                while True:
                    if new_task_name.casefold().strip() == old_name.casefold().strip():
                        print("The new name can't be the same as the old one.")
                        new_task_name = input("Enter the new task name: ").strip()
                    else:
                        break
                edit_task(tasks, task_number, new_task_name)
                save_tasks(tasks, TASKS_FILE)
                print(f"Task {task_number} renamed to '{new_task_name}'.")
            except EmptyTaskError as e:
                print(f"Error: {e} Try again.")
            except ValueError:
                print("Error: You must enter a valid number.")
            except TaskNotFoundError as e:
                print(f"Error: task {e} does not exist.")
        elif option == "6":
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please select a valid option.")


if __name__ == "__main__":
    main()