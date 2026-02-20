from queue import PriorityQueue as Priority_Queue
import json

current_tasks = dict()
priority_idx = Priority_Queue()
number_retrieved = 0

FIRST_ID = 1

# Id to be given to the next task
newest_id = FIRST_ID

def validate_task(description, priority):
    messages = []

    if not description:
        messages.append("Field 'description' must be given")

    if not priority:
        messages.append("Field 'priority' must be given")

    try:
        priority = int(priority)
        if priority < 0:
            messages.append("Field 'priority' must be greater than, or equal to, 0")

    except ValueError:
        messages.append("Field 'priority' must be a number")

    return messages

# POINT: Returns list instead of bool for consistency in validation/errors
def validate_id(id):
    messages = []

    try:
        id = int(id)
        
        if id < FIRST_ID:
            messages.append(f"Field 'id' must be greater than or equal to ${FIRST_ID}")

        found_task = get_task_by_id()
        if not found_task:
            messages.append(f"There is no task with the id '${id}'")

    except ValueError:
        messages.append("Field 'id' must be a number")

    return messages, found_task

# POINT: Emphasises error messages with trailing blank line and trailing ***
def print_error_messages(messages):
    print()

    for msg in messages:
        print(f"*** ERROR: ${msg} *** ")
    
    print()

def load_tasks():
    # TODO: Change state management to class to improve readability
    global current_tasks, number_retrieved  # POINT: Bad practice- difficult to read.
    with open("tasks.json") as f: # POINT: Used with statement to prevent leaks
        tasksJSON = json.load(f)
        current_tasks, number_retrieved = tasksJSON["tasks", "number_retrieved"]    # POINT: Storing number_retrieved simplifies logic and reduces stored data

        reset_task_queue(number_retrieved)


def save_tasks():
    print("Saving. Do not close the program...") # Print inside save_tasks() to ensure that the user always knows when the program last saved
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
    number_retrieved += 1
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

def reset_task_queue(number_retrieved=0):
    for id, task in current_tasks.items():
        if id > len(current_tasks) - number_retrieved:  # POINT: Fragile- works only if no tasks can be deleted
            break

        priority_idx.put_nowait((task["priority"], task["id"]))

user_choice = None
while True:

    print("\n========== What would you like to do? ==========")
    print("1: Add a new task")
    print("2: Retrieve next task")
    print("3: Retrieve task by ID")
    print("4: Mark a task as complete")
    print("5: Reset task queue")
    print("quit: Exit program")
    user_choice = input("\nchoice: ")
    
    match user_choice:

        # Add task
        case "1":
            description = input("Enter a description for the new task: ")
            priority = input("Enter a priority for the new task: ")

            messages = validate_task(description, priority)
            if messages:
                print_error_messages(messages)
                pass 

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

            messages, found_task = validate_id(id)
            if messages:
                print_error_messages(messages)
                pass

            print(found_task)

        # Complete task
        case "4":
            id = input("Enter the task's id: ")

            messages, _ = validate_id(id)
            if messages:
                print_error_messages(messages)
                pass

            task = complete_task(int(id))
            print(task)

        # Reset the task queue to be as if nothing was retrieved
        case "5":

            if number_retrieved == 0:
                print("No tasks have been retrieved from the queue- no change")

            print("Resetting task queue...")
            reset_task_queue()
            print("Resetting complete")

        # Exit program
        case "quit":
            print("Shutting down...")
            break

        case _:
            print_error_messages(["You must choose 1, 2, 3, 4, or 5"])


quit()

# POINT: Optimise by deleting tasks of a certain age
# POINT: Optimise by making autosave optional