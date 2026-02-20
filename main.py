from queue import PriorityQueue as Priority_Queue
import json

current_tasks = dict()
priority_idx = Priority_Queue()
number_retrieved = 0

# Id to be given to the nexdt task
newest_id = 1

def load_tasks():
    # TODO: Change state management to class to improve readability
    global current_tasks, number_retrieved  # POINT: Bad practice- difficult to read.
    with open("tasks.json") as f: # POINT: Used with statement to prevent leaks
        tasksJSON = json.load(f)
        current_tasks, number_retrieved = tasksJSON["tasks", "number_retrieved"]    # POINT: Storing number_retrieved simplifies logic and reduces stored data

        for id, task in current_tasks.items():
            if id > len(current_tasks) - number_retrieved:  # POINT: Fragile- works only if no tasks can be deleted
                break

            priority_idx.put_nowait((task["priority"], task["id"]))


def save_tasks():
    with open("tasks.json") as f:
        json.dump({
            "current_tasks": current_tasks,
            "number_retrieved": number_retrieved
        }, f)

def add_task(description, priority):
    new_task = {
        "id": newest_id,
        "description": description,
        "priority": priority,
        "status": "Incomplete"
    }

    current_tasks[new_task["id"]] = new_task
    priority_idx.put_nowait((new_task["priority"], new_task["id"]))

    save_tasks()

    return current_tasks[new_task["id"]]

# TODO: Skip completed tasks
def get_task_by_priority():
    if priority_idx.empty():
            return {}

    priority_task = priority_idx.get_nowait()
    next_task = current_tasks[priority_task[1]]

    save_tasks()    # POINT: Autosave trades performance for ensuring that tasks are always safe 

    return next_task

def get_task_by_id(id):
    found_task = current_tasks.get(id, {}) # Retrieve the task safely. Return {} if doesn't exist
    return found_task

def complete_task(id):
    current_tasks[id]["status"] = "Complete"
    save_tasks()

    return current_tasks[id]

user_choice = None
while True:

    print("\n========== What would you like to do? ==========")
    print("1: Add a new task")
    print("2: Retrieve next task")
    print("3: Retrieve task by ID")
    print("4: Mark a task as complete")
    print("quit: Exit program")
    user_choice = input("\nchoice: ")
    
    match user_choice:

        # Add task
        case "1":
            description = input("Enter a description for the new task: ")
            priority = input("Enter a priority for the new task: ")

            new_task = add_task(description, int(priority))
            newest_id += 1
            print(new_task)

        # Get task by priority
        case "2":
            next_task = get_task_by_priority()
            print(next_task)
            pass

        
        # Get task by id
        case "3":
            id = input("Enter the task's id: ")

            found_task = get_task_by_id(int(id))

            print(found_task)

        # Complete task
        case "4":
            id = input("Enter the task's id: ")

            task = complete_task(int(id))
            print(task)

        # Exit program
        case "quit":
            print("Shutting down...")
            break

        # Basic feedback to reduce ambiguity for POC tester
        case _:
            print("You must choose 1, 2, 3, or 4")


quit()

# POINT: Optimise by deleting tasks of a certain age
# POINT: Optimise by making autosave optional