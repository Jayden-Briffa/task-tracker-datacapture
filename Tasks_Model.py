
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
        # Empty the state and save if starting fresh
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
        
        # Using with statement to ensure file is always closed after opening
        with open("task_data.json", "w") as f:
            json.dump({
                "current_tasks": self.current_tasks,
                "number_retrieved": self.number_retrieved,
                "newest_id": self.newest_id
            }, f, indent=4)

    def load_tasks(self):
        try:
            print("Loading tasks...")
            
            with open("task_data.json", "r") as f:
                tasksJSON = json.load(f)
                self.current_tasks = tasksJSON["current_tasks"]
                self.number_retrieved = tasksJSON["number_retrieved"]
                self.newest_id = tasksJSON["newest_id"]

                # Reconstruct priority_idx based on number_retrieved and current_tasks
                self.reset_task_queue(self.number_retrieved)

        except FileNotFoundError:
            print("No saved tasks found. Starting with empty task list...")
            self.save_tasks(no_print=True) # No need to tell the user we're saving since we're just creating the file

    def add_task(self, description: str, priority: int, is_complete=False, no_save=False) -> dict:
        new_task = {
            "id": str(self.newest_id),
            "description": description,
            "priority": int(priority),
            "status": "Complete" if is_complete else "Incomplete"
        }

        # Add task to current_tasks, then add to priority queue
        self.current_tasks[new_task["id"]] = new_task
        self.priority_idx.put_nowait((new_task["priority"], new_task["id"]))
                
        # Called 'newest_id' to prevent confusion with id of next task to be retrieved
        self.newest_id += 1

        if not no_save:
            self.save_tasks()

        return self.current_tasks[new_task["id"]]
    
    def get_task_by_priority(self, no_save=False) -> dict:
        while True:
            if self.priority_idx.empty():
                return {}
            
            priority_task = self.priority_idx.get_nowait()
            next_task = self.current_tasks[priority_task[1]]
            
            if next_task["status"] == "Incomplete":
                self.number_retrieved += 1
                if not no_save:
                    self.save_tasks() 

                return next_task
        
    def get_task_by_id(self, id) -> dict:
        found_task = self.current_tasks.get(id, {}) # Retrieve the task safely. Return {} if doesn't exist
        return found_task

    def complete_task(self, id) -> dict:
        # Status is a string instead of a boolean for easier printing and readability
        self.current_tasks[id]["status"] = "Complete"
        self.save_tasks()

        return self.current_tasks[id]

    def reset_task_queue(self, number_retrieved=0, no_save=False):
        self.number_retrieved = number_retrieved
        self.priority_idx = Priority_Queue()
        
        # Reconstruct the full queue
        for task in self.current_tasks.values():
            self.priority_idx.put_nowait((task["priority"], task["id"]))
            
        # Call get_task_by_priority number_retrieved times
        for _ in range(self.number_retrieved):
            self.get_task_by_priority(no_save=True)

        if not no_save:
            self.save_tasks(no_print=True)
