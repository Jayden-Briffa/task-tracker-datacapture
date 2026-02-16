# How to run the program
Run:
py main.py
OR
python3 main.py

# 1. Add new tasks
When prompted, enter "1" on the main menu then enter the following fields:
- Description (string)- Core content of the task
- Priority (integer)- The lower the number, the earlier it appears in the priority queue

A task id will be automatically generated and the new task will be passed into memory storage.

**Example output**
```
Task successfully created!
--id: 5
--description: Review ticket #1234
--priority: 1
--status: "Incomplete"
```

# 2. Retrieve the next task based on priority
When prompted, enter "2" on the main menu. There are no inputs. If there are still tasks in the queue, the one with the next highest priority (the lowest priority value) will be outputted and removed from the queue.

**Example output**
```
--id: 5
--description: Review ticket #1234
--priority: 0
--status: "Complete"
```

# 3. Retrieve tasks by ID
When prompted, enter "3" on the main menu then enter the following fields:
- Id (integer)- The id of the task you wish to retrieve

**Example output**
```
--id: 5
--description: Review ticket #1234
--priority: 1
--status: "Complete"
```

# 4. Mark tasks as complete
When prompted, enter "4" on the main menu then enter the following fields:
- Id (integer)- The id of the task you wish to mark

The status of the given task will be flipped to say "Complete" instead of "Incomplete"

**Example output**
```
--id: 5
--description: Review ticket #1234
--priority: 1
--status: "Complete"
```

# 5. Quit
When prompted, enter "quit" on the main menu and you will stop the program running