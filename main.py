from Tasks_Model import Tasks_Model

def output_task(task):
    print_task_color = lambda text: print(f"\033[93m {text}\033[00m")
    print_task_color(f"---- Task #{task['id']} ({task['status']}) ----")
    print_task_color(f"-- Description: {task['description']}")
    print_task_color(f"-- Priority: {task['priority']}")

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
        messages.append("Field 'priority' must be an integer")

    return messages

# POINT: Returns list instead of bool for consistency in validation/errors
def validate_id(id, model):
    messages = []
    found_task = {}

    try:
        intId = int(id)
        
        if intId < Tasks_Model.FIRST_ID:
            messages.append(f"Field 'id' must be greater than or equal to {Tasks_Model.FIRST_ID}")

        found_task = model.get_task_by_id(id)
        if not found_task:
            messages.append(f"There is no task with the id '{id}'")

    except ValueError:
        messages.append("Field 'id' must be an integer")

    return messages, found_task

# POINT: Emphasises error messages with trailing blank line and trailing ***
def print_error_messages(messages):
    print()

    for msg in messages:
        print(f"*** \033[91m ERROR\033[00m: {msg} *** ")
    
    print()

def main(model: Tasks_Model = None):
    if model == None:
        model = Tasks_Model()

    user_choice = None
    while True:

        print("========== What would you like to do? ==========")
        print("1: Add a new task")
        print("2: Retrieve next task")
        print("3: Retrieve task by ID")
        print("4: Mark a task as complete")
        print("5: Reset task queue")
        print("quit: Exit program")
        user_choice = input("\nEnter a choice: ")
        
        match user_choice:

            # Add task
            case "1":
                description = input("Enter a description for the new task: ")
                priority = input("Enter a priority for the new task: ")

                messages = validate_task(description, priority)
                if messages:
                    print_error_messages(messages)
                    continue 

                new_task = model.add_task(description, int(priority))
                print("Task created successfully:")
                output_task(new_task)

            # Get task by priority
            case "2":
                next_task = model.get_task_by_priority()
                if not next_task:
                    print_error_messages(["There are no tasks in the queue. Try resetting the task queue, or adding a new task."])
                    continue

                print("Next task retrieved successfully:")
                output_task(next_task)

            # Get task by id
            case "3":
                id = input("Enter the task's id: ")

                messages, found_task = validate_id(id, model)
                if messages:
                    print_error_messages(messages)
                    continue
                
                print("Task retrieved successfully:")
                output_task(found_task)

            # Complete task
            case "4":
                id = input("Enter the task's id: ")

                messages, found_task = validate_id(id, model)
                if messages:
                    print_error_messages(messages)
                    continue

                if found_task["status"] == "Complete":
                    print_error_messages([f"Task with id '{id}' is already complete"])
                    continue

                task = model.complete_task(id)
                print("Task marked as complete successfully:")
                output_task(task)

            # Reset the task queue to be as if nothing was retrieved
            case "5":
                if model.number_retrieved == 0:
                    print_error_messages(["No tasks have been retrieved from the queue- no change"])
                    continue

                print("Resetting task queue...")
                model.reset_task_queue()
                print("Resetting complete")

            # Exit program
            case "quit":
                print("Shutting down...")
                break

            case _:
                print_error_messages(["You must choose 1, 2, 3, 4, or 5"])


    quit()

if __name__ == "__main__":
    main()
   

# POINT: Optimise by deleting tasks of a certain age
# POINT: Optimise by making autosave optional
# POINT: Optimise by only saving on program close