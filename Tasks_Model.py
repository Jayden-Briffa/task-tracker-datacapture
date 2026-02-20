
from queue import PriorityQueue as Priority_Queue
import json

class Tasks_Model:
    FIRST_ID = 1

    current_tasks = dict()
    priority_idx = Priority_Queue()
    number_retrieved = 0

    # Id to be given to the next task
    newest_id = FIRST_ID

    def __init__(self, start_fresh=False):
        if start_fresh:
            self.current_tasks = dict()
            self.priority_idx = Priority_Queue()
            self.number_retrieved = 0
            self.newest_id = self.FIRST_ID
            self.save_tasks(no_print=True)

        self.load_tasks()
    
    def save_tasks(self, no_print=False):
        if not no_print:
            print("Saving. Do not close the program...") 

        with open("task_data.json", "w") as f:
            json.dump({
                "current_tasks": self.current_tasks,
                "number_retrieved": self.number_retrieved,
                "newest_id": self.newest_id
            }, f)

    def load_tasks(self):
        try:
            print("Loading tasks...")
            with open("task_data.json", "r") as f: # POINT: Used with statement to prevent leaks
                tasksJSON = json.load(f)
                self.current_tasks = tasksJSON["current_tasks"]
                self.number_retrieved = tasksJSON["number_retrieved"]
                self.newest_id = tasksJSON["newest_id"]

                self.reset_task_queue(self.number_retrieved)

        except FileNotFoundError:
            print("No saved tasks found. Starting with empty task list...")
            self.save_tasks(no_print=True)

    def add_task(self, description: str, priority: int, is_complete=False, no_save=False):
        new_task = {
            "id": str(self.newest_id),
            "description": description,
            "priority": int(priority),
            "status": "Complete" if is_complete else "Incomplete"
        }

        self.current_tasks[new_task["id"]] = new_task
        self.priority_idx.put_nowait((new_task["priority"], new_task["id"]))
                
        self.newest_id += 1

        if not no_save:
            self.save_tasks()

        return self.current_tasks[new_task["id"]]
    
    def get_task_by_priority(self, no_save=False):
        if self.priority_idx.empty():
                return {}

        while True:
            priority_task = self.priority_idx.get_nowait()
            next_task = self.current_tasks[priority_task[1]]
            
            if next_task["status"] == "Incomplete":
                self.number_retrieved += 1
                
                if not no_save:
                    self.save_tasks()    # POINT: Autosave trades performance for ensuring that tasks are always safe 

                return next_task
        
    def get_task_by_id(self, id):
        found_task = self.current_tasks.get(id, {}) # Retrieve the task safely. Return {} if doesn't exist
        return found_task

    def complete_task(self, id):
        self.current_tasks[id]["status"] = "Complete"
        self.save_tasks()

        return self.current_tasks[id]

    def reset_task_queue(self, number_retrieved=0, no_save=False):
        self.priority_idx = Priority_Queue()

        for task in self.current_tasks.values():
            self.priority_idx.put_nowait((task["priority"], task["id"]))

        for _ in range(number_retrieved):
            self.priority_idx.get_nowait()

        if number_retrieved == 0 and not no_save:
            self.save_tasks(no_print=True)
