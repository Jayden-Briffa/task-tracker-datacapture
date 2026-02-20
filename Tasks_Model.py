
from queue import PriorityQueue as Priority_Queue
import json

class Tasks_Model:
    FIRST_ID = 1

    current_tasks = dict()
    priority_idx = Priority_Queue()
    number_retrieved = 0

    # Id to be given to the next task
    newest_id = FIRST_ID

    def __init__(self):
        self.load_tasks()
    
    def save_tasks(self):
        print("Saving. Do not close the program...") # Print inside save_tasks() to ensure that the user always knows when the program last saved
        with open("tasks.json", "w") as f:
            json.dump({
                "current_tasks": self.current_tasks,
                "number_retrieved": self.number_retrieved
            }, f)

    def load_tasks(self):
        try:
            with open("tasks.json", "r") as f: # POINT: Used with statement to prevent leaks
                tasksJSON = json.load(f)
                self.current_tasks = tasksJSON["current_tasks"]
                self.number_retrieved = tasksJSON["number_retrieved"]

                self.reset_task_queue(self.number_retrieved)
        except FileNotFoundError:
            print("No saved tasks found. Starting with empty task list.")
            self.save_tasks()

    def add_task(self, description, priority):
        new_task = {
            "id": self.newest_id,
            "description": description,
            "priority": priority,
            "status": "Incomplete"
        }

        self.current_tasks[new_task["id"]] = new_task
        self.priority_idx.put_nowait((new_task["priority"], new_task["id"]))

        self.save_tasks()

        return self.current_tasks[new_task["id"]]
    
    # TODO: Skip completed tasks
    def get_task_by_priority(self):
        if self.priority_idx.empty():
                return {}

        priority_task = self.priority_idx.get_nowait()
        self.number_retrieved += 1
        next_task = self.current_tasks[priority_task[1]]

        self.save_tasks()    # POINT: Autosave trades performance for ensuring that tasks are always safe 

        return next_task
    
    def get_task_by_id(self, id):
        found_task = self.current_tasks.get(id, {}) # Retrieve the task safely. Return {} if doesn't exist
        return found_task

    def complete_task(self, id):
        self.current_tasks[id]["status"] = "Complete"
        self.save_tasks()

        return self.current_tasks[id]

    def reset_task_queue(self, number_retrieved=0):
        for id, task in self.current_tasks.items():
            if id > len(self.current_tasks) - number_retrieved:  # POINT: Fragile- works only if no tasks can be deleted
                break

            self.priority_idx.put_nowait((task["priority"], task["id"]))