# Overview
This project has been created to allow DataCapture to store and retrieve tasks. Tasks are stored in a JSON format and they are saved automatically
## General usage
Run:
```bash 
py main.py
# OR
python3 main.py
```

You will be shown a menu containing 6 options (see Key Functionality for more details). Type the number corresponding to your choice and follow any instructions afterward.

## Dependencies
This project is dependency-free

# Key functionality
## 1. Add new tasks
When prompted, enter "1" on the main menu then enter the following fields:
- Description (string)- Core content of the task
- Priority (integer)- The lower the number, the earlier it appears in the priority queue

A task id will be automatically generated and the new task will be passed into memory storage.

**Example output**
```
--- Task created successfully: ---
 ---- Task #2 (Incomplete) ----
 -- Description: my description
 -- Priority: 2
```

## 2. Retrieve the next task based on priority
When prompted, enter "2" on the main menu. There are no inputs. If there are still tasks in the queue, the one with the next highest priority (the lowest priority value) will be outputted and removed from the queue.

**Example output**
```
Next task retrieved successfully:
 ---- Task #2 (Incomplete) ----
 -- Description: my description
 -- Priority: 2
```

## 3. Retrieve tasks by ID
When prompted, enter "3" on the main menu then enter the following fields:
- Id (integer)- The id of the task you wish to retrieve

**Example output**
```
--- Task retrieved successfully: ---
 ---- Task #1 (Incomplete) ----
 -- Description: my description
 -- Priority: 2
```

## 4. Mark tasks as complete
When prompted, enter "4" on the main menu then enter the following fields:
- Id (integer)- The id of the task you wish to mark

The status of the given task will be flipped to say "Complete" instead of "Incomplete"

**Example output**
```
--- Task marked as complete successfully: ---
 ---- Task #2 (Complete) ----
 -- Description: apple
 -- Priority: 2
```

## 5. Reset task queue
When prompted, enter "5" on the main menu. There are no inputs. If tasks were taken from the queue, they will be restored and you can retrieve them again.

**Example output**
```
Resetting task queue...
--- Resetting complete ---
```

## Quit
When prompted, enter "quit" on the main menu and you will stop the program running

# Testing
This project was tested with manual testing (see ./planning/Test plan.docx and ./planning/Test table.docx), but a simple test script (test.py) was made to assist in repetitive performance tests