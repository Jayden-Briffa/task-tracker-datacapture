# Validation functions to check user input and model state before performing key actions. Each function returns a list of error messages... 
# which is empty if there are no errors.
def validate_task(description, priority) -> list[str]:
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

# Returns a found task for convenience
# Takes dynamic first_id and get_task_func for easier testing and future development
def validate_id(id, first_id, get_task_func) -> tuple[list[str], dict]:
    messages = []
    found_task = {}

    try:
        intId = int(id)
        
        if intId < first_id:
            messages.append(f"Field 'id' must be greater than or equal to {first_id}")

        found_task = get_task_func(id)
        if not found_task:
            messages.append(f"There is no task with the id '{id}'")

    except ValueError:
        messages.append("Field 'id' must be an integer")

    return messages, found_task

# Simple validation checks- still return a list of messages for consistency with other validation functions
def validate_queue_returned_next_task(next_task) -> list[str]:
    messages = []
    if not next_task:
        messages.append("There are no tasks in the queue. Try resetting the task queue, or adding a new task.")
    return messages

def validate_task_not_complete(task) -> list[str]:
    messages = []
    if task["status"] == "Complete":
        messages.append(f"Task with id '{task['id']}' is already complete")
    return messages

def validate_some_retrieved(number_retrieved) -> list[str]:
    messages = []
    if number_retrieved == 0:
        messages.append("No tasks have been retrieved from the queue- no change")
    return messages