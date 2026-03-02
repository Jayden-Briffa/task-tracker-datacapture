
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
# POINT accepts first_id and get_task_func to decouple from Tasks_Model
def validate_id(id, first_id, get_task_func):
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

def validate_queue_returned_next_task(next_task):
    messages = []
    if not next_task:
        messages.append("There are no tasks in the queue. Try resetting the task queue, or adding a new task.")
    return messages

def validate_task_not_complete(task):
    messages = []
    if task["status"] == "Complete":
        messages.append(f"Task with id '{task['id']}' is already complete")
    return messages

def validate_some_retrieved(number_retrieved):
    messages = []
    if number_retrieved == 0:
        messages.append("No tasks have been retrieved from the queue- no change")
    return messages