from queue import PriorityQueue as Priority_Queue

current_tasks = dict()
priority_idx = Priority_Queue()

# Id to be given to the nexdt task
newest_id = 0

def add_task(description, priority):
    new_task = {
        "id": newest_id,
        "description": description,
        "priority": priority,
        "status": "Incomplete"
    }

    current_tasks[new_task["id"]] = new_task
    priority_idx.put_nowait((new_task["priority"], new_task["id"]))

    return current_tasks[new_task["id"]]

def get_task_by_priority():
    if priority_idx.empty():
            return {}

    priority_task = priority_idx.get_nowait()
    next_task = current_tasks[priority_task[1]]

    return next_task

def get_task_by_id(id):
    found_task = current_tasks.get(id, {}) # Retrieve the task safely. Return {} if doesn't exist
    return found_task

def complete_task(id):
    current_tasks[id]["status"] = "Complete"
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