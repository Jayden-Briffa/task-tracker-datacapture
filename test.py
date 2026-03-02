from main import main
from Tasks_Model import Tasks_Model
import time

# Empty all data in task_data.json before testing
model = Tasks_Model(True)

# Create num_tasks tasks with varying completion status
num_tasks = 10000
for i in range(num_tasks-1):
    is_complete = False
    # is_complete = i == int(num_tasks/2) # Every task is incomplete except the middle one
    # is_complete = i % 3 != 0 # Every 3rd task is complete, the rest are incomplete
    model.add_task(f"Task {i}", 2, is_complete=is_complete, no_save=True)

start = time.time()
model.get_task_by_priority(no_save=True) # Replace with operation, e.g., model.get_task_by_priority()
end = time.time()
operation_time = end-start
print(f"Time taken to process: {operation_time} seconds")

# Isolate save time to find operation time without saving
start = time.time()
model.save_tasks()
end = time.time()
print(f"Time taken to save tasks: {end-start} seconds")
print(f"Total time taken: {operation_time + (end-start)} seconds")