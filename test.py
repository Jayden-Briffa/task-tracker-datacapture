from main import main
from Tasks_Model import Tasks_Model
import time

model = Tasks_Model(True)

num_tasks = 100000
for i in range(num_tasks-1):
    is_complete = i != int(num_tasks/2)
    model.add_task(f"Task {i}", 2, is_complete=is_complete, no_save=True)

start = time.time()
model.reset_task_queue(no_save=True) # Replace with process, e.g., model.get_task_by_priority()
end = time.time()
total_time = end-start
print(f"Time taken to process: {end-start} seconds")

start = time.time()
model.save_tasks()
end = time.time()
print(f"Time taken to save tasks: {end-start} seconds")
print(f"Total time taken: {total_time + (end-start)} seconds")