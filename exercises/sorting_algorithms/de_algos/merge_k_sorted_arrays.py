import pandas as pd

def get_exercise():
    return {
        "title": "Merge K Sorted Arrays (9/10)",
        "subtitle": "Queues / Priority Queues, Loops, Arrays / Lists",
        "description": "Imagine 3 parallel distributed worker nodes outputting individually sorted IDs. You are given a DataFrame where each row is a list of these sorted IDs from a worker. Efficiently merge all these arrays into one single sorted list.",
        "data": pd.DataFrame({"worker_arrays": [[1, 4, 7], [2, 5, 8], [3, 6, 9, 10]]}),
        "allowed_modes": ["Python"],
        "hint_python": "Use a Priority Queue (Min-Heap). Insert the first element of each array into the heap alongside its array index and element index. Pop the minimum, add to result, and insert the next element from that specific array into the heap.",
        "solution_python": """import heapq

def merge_k_sorted_arrays(arrays):
    min_heap = []
    result = []
    
    # Intialize heap with the first element of each array
    # Tuple format: (value, array_index, element_index)
    for i, arr in enumerate(arrays):
        if arr:
            heapq.heappush(min_heap, (arr[0], i, 0))
            
    while min_heap:
        val, arr_idx, ele_idx = heapq.heappop(min_heap)
        result.append(val)
        
        # If the array has more elements, push the next one
        if ele_idx + 1 < len(arrays[arr_idx]):
            next_val = arrays[arr_idx][ele_idx + 1]
            heapq.heappush(min_heap, (next_val, arr_idx, ele_idx + 1))
            
    return result

worker_arrays = df['worker_arrays'].tolist()
result = merge_k_sorted_arrays(worker_arrays)
""",
        "deep_dive": "This mimics the 'Shuffle & Sort' phase of distributed compute engines like Apache Hadoop or Spark. Using a Min-Heap guarantees an O(N log K) time complexity where N is the total elements and K is the number of arrays, maintaining a very small O(K) memory footprint."
    }
