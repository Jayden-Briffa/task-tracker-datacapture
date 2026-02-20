from Tasks_Model import Tasks_Model

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
        
        if id < Tasks_Model.FIRST_ID:
            messages.append(f"Field 'id' must be greater than or equal to ${Tasks_Model.FIRST_ID}")

        found_task = model.get_task_by_id(id)
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

if __name__ == "__main__":
    model = Tasks_Model()

    user_choice = None
    while True:

        print("\n========== What would you like to do? ==========")
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
                    pass 

                new_task = model.add_task(description, int(priority))
                newest_id += 1
                print(new_task)

            # Get task by priority
            case "2":
                next_task = model.get_task_by_priority()
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

                task = model.complete_task(int(id))
                print(task)

            # Reset the task queue to be as if nothing was retrieved
            case "5":

                if model.number_retrieved == 0:
                    print("No tasks have been retrieved from the queue- no change")

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

# POINT: Optimise by deleting tasks of a certain age
# POINT: Optimise by making autosave optional