import pandas as pd

def get_exercise():
    return {
        "title": "Min/Max Priority Queue Job Scheduler (8/10)",
        "description": "You are building a basic Task Scheduler. You are given a DataFrame column 'tasks' containing lists of `[priority_score, task_name]`. Create a Priority Queue that outputs tasks in DESCENDING priority order (Max-Heap behavior). Process all tasks and return an ordered list of only the `task_name` strings.",
        "data": pd.DataFrame({"tasks": [[3, "ETL Extract"], [10, "Database Crash Alert"], [1, "Daily Report"], [7, "Log Rotation"]]}),
        "allowed_modes": ["Python"],
        "hint_python": "Python's `heapq` only provides a Min-Heap. To simulate a Max-Heap for descending extraction, push the `priority_score` in as a negative number `-score`.",
        "solution_python": """import heapq

def process_task_queue(tasks):
    max_heap = []
    
    # Store items in heap negating the score for max-heap behavior
    for score, name in tasks:
        heapq.heappush(max_heap, (-score, name))
        
    result_names = []
    # Pop items out until empty
    while max_heap:
        negative_score, name = heapq.heappop(max_heap)
        result_names.append(name)
        
    return result_names

tasks_list = df['tasks'].tolist()
result = process_task_queue(tasks_list)
""",
        "deep_dive": "Priority Queues govern almost all Airflow scheduling, Kafka partitioning, and streaming rate limiting rules under the hood. Knowing how to forcefully invert standard data structure behaviors (like `-score` for a min-heap) is a common analytical test."
    }
