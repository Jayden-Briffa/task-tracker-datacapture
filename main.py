from Tasks_Model import Tasks_Model
from validation import validate_queue_returned_next_task, validate_some_retrieved, validate_task, validate_id, validate_task_not_complete
# TODO: Add comments
def output_task(task):
    print_task_color = lambda text: print(f"\033[93m {text}\033[00m")
    print_task_color(f"---- Task #{task['id']} ({task['status']}) ----")
    print_task_color(f"-- Description: {task['description']}")
    print_task_color(f"-- Priority: {task['priority']}")

# POINT: Emphasises error messages with trailing blank line and trailing ***
def output_error_messages(messages):
    print()

    for msg in messages:
        print(f"*** \033[91mERROR: {msg}\033[00m  *** ")
    
    print()

def output_success(msg):
    print(f"--- \033[92m{msg}\033[00m ---")

# POINT: Dynamic model allows for easier testing and scalability
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
                    output_error_messages(messages)
                    continue 

                new_task = model.add_task(description, int(priority))
                output_success("Task created successfully:")
                output_task(new_task)

            # Get task by priority
            case "2":
                next_task = model.get_task_by_priority()
                messages = validate_queue_returned_next_task(next_task)
                if messages:
                    output_error_messages(messages)
                    continue

                output_success("Next task retrieved successfully:")
                output_task(next_task)

            # Get task by id
            case "3":
                id = input("Enter the task's id: ")

                messages, found_task = validate_id(id, model.FIRST_ID, model.get_task_by_id)
                if messages:
                    output_error_messages(messages)
                    continue
                
                output_success("Task retrieved successfully:")
                output_task(found_task)

            # Complete task
            case "4":
                id = input("Enter the task's id: ")

                messages, found_task = validate_id(id, model.FIRST_ID, model.get_task_by_id)
                if messages:
                    output_error_messages(messages)
                    continue

                messages = validate_task_not_complete(found_task)
                if messages:
                    output_error_messages(messages)
                    continue

                task = model.complete_task(id)
                output_success("Task marked as complete successfully:")
                output_task(task)

            # Reset the task queue to be as if nothing was retrieved
            case "5":
                messages = validate_some_retrieved(model.number_retrieved)
                if messages:    
                    output_error_messages(messages)
                    continue

                print("Resetting task queue...")
                model.reset_task_queue()
                output_success("Resetting complete")

            # Exit program
            case "quit":
                print("Shutting down...")
                break

            case _:
                output_error_messages(["You must choose 1, 2, 3, 4, 5, or 'quit'"])

    quit()

if __name__ == "__main__":
    main()

# POINT: Optimise by deleting tasks of a certain age
# POINT: Optimise by making autosave optional
# POINT: Optimise by only saving on program close
# POINT: Optimise by implementing more robust error checks after each key action
# POINT: Optimise by allowing color optionality for better accessibility
# POINT: Get-by-priority was the biggest challenge because it required careful state management and would cause a catastrphic error if anything went wrong.
# POINT: Optimise by reducing coupling between output and task object by creating a task object with its own output method