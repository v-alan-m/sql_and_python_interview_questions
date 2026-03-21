import pandas as pd

def get_exercise():
    return {
        "title": "Min/Max Priority Queue Job Scheduler (8/10)",
        "subtitle": "Queues / Priority Queues, Loops, Arrays / Lists",
        "description": "You are building a basic Task Scheduler. You are given a DataFrame column 'tasks' containing dictionaries of `{'score': int, 'name': str}`. Create a Priority Queue that outputs tasks in DESCENDING priority order (Max-Heap behavior). Process all tasks and return an ordered list of only the `task_name` strings.",
        "data": pd.DataFrame({"tasks": [{"score": 3, "name": "ETL Extract"}, {"score": 10, "name": "Database Crash Alert"}, {"score": 1, "name": "Daily Report"}, {"score": 7, "name": "Log Rotation"}]}),
        "allowed_modes": ["Python"],
        "hint_python": "Python's `heapq` only provides a Min-Heap. To simulate a Max-Heap for descending extraction, push the `priority_score` in as a negative number `-score`.",
        "solution_python": """import heapq

def process_task_queue(tasks):
    max_heap = []
    
    # Store items in heap negating the score for max-heap behavior
    for task in tasks:
        heapq.heappush(max_heap, (-task['score'], task['name']))
        
    result_names = []
    # Pop items out until empty
    while max_heap:
        negative_score, name = heapq.heappop(max_heap)
        result_names.append(name)
        
    return result_names

tasks_list = df['tasks'].tolist()
result = process_task_queue(tasks_list)
""",
        "deep_dive": "Priority Queues govern almost all Airflow scheduling, Kafka partitioning, and streaming rate limiting rules under the hood. Knowing how to forcefully invert standard data structure behaviors (like `-score` for a min-heap) is a common analytical test.",
        "big_o_explanation": "### Time Complexity: $O(N \\log N)$\nWhere **$N$** is the number of tasks in the queue.\n- Pushing each task into the heap takes $O(\\log N)$ time, and we do this $N$ times, taking $O(N \\log N)$ time.\n- Popping each task from the heap also takes $O(\\log N)$ time, done $N$ times, totaling $O(N \\log N)$ time.\n- Thus, the overall time complexity is $O(N \\log N)$.\n\n### Space Complexity: $O(N)$\n- The heap data structure stores all $N$ tasks, requiring $O(N)$ auxiliary space.\n\n### Optimization Context\nIf we were to sort the entire list of tasks first, it would take $O(N \\log N)$ time, which is comparable. However, the fundamental advantage of a Priority Queue/Heap is its ability to handle **streaming data**. If tasks arrive continuously, a heap allows us to insert a new task in $O(\\log N)$ time and extract the highest priority task in $O(\\log N)$ time, without needing to re-sort the entire list. Priority Queues are the backbone of dynamic scheduling systems because they optimize for continuous state changes rather than static batch processing."
    }
