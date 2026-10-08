#   Task Manager CLI

A command-line task manager that saves your tasks to a JSON file, so they aren't lost when you close the program.

##  Features

- Add, list and complete tasks from an interactive menu
- Tasks persist between sessions (saved in `tasks.json`)
- Rejects empty task names
- If the data file is corrupted, it saves a copy (`tasks.json.bak`) and starts with an empty list

##  Requirements

- Python 3.11+ (tested on 3.15)
- No external libraries required

##  Installation

```bash
git clone https://github.com/ItsGeno/task-manager-cli.git
cd task-manager-cli
```

##  Usage

```bash
python main.py
```

Example:

```
Options:
1. Add task
2. List tasks
3. Complete task
4. Exit
Select an option: 1
Enter the task name: Buy bread
Task 'Buy bread' added.

Select an option: 2

Task list:
1. Buy bread - [ ]

Select an option: 3
Enter the number of the task to complete: 1
Task number 1 completed.
```

##  Error handling

| Case                   | Message                                            |
|------------------------|----------------------------------------------------|
| Empty task name        | `Error: The task name cannot be empty. Try again.` |
| Invalid number         | `Error: You must enter a valid number.`            |
| Task does not exist    | `Error: task 5 does not exist.`                    |
| Task already completed | `Error: task 1 is already completed.`              |
| Corrupted data file    | `Error: The tasks file is corrupted...`            |

##  Data

Tasks are stored in `tasks.json`, in the folder where you run the program. The file is created automatically when you add your first task.

##  Roadmap

- [X] Delete tasks
- [ ] Edit a task name
- [ ] Filter by pending and completed

##  Built with

- Python (standard library: `json` and `shutil`)

##  About

Practice project to sharpen my Python skills.