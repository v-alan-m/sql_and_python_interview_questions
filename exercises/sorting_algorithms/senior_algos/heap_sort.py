import pandas as pd

def get_exercise():
    return {
        "title": "Heap Sort (6/10)",
        "subtitle": "Queues / Priority Queues, Loops, Arrays / Lists",
        "description": "Implement the Heap Sort algorithm. You are given a DataFrame with a single column 'numbers'. Sort the numbers in ascending order and return the result as a list.",
        "data": pd.DataFrame({"numbers": [12, 11, 13, 5, 6, 7]}),
        "allowed_modes": ["Python"],
        "hint_python": "First build a max heap from the input data. Then repeatedly extract the maximum element and place it at the end of the sorted array.",
        "solution_python": """def heapify(arr, n, i):
    largest = i
    l = 2 * i + 1
    r = 2 * i + 2
    
    if l < n and arr[l] > arr[largest]:
        largest = l
        
    if r < n and arr[r] > arr[largest]:
        largest = r
        
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]
        heapify(arr, n, largest)

def heap_sort(arr):
    n = len(arr)
    
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)
        
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]
        heapify(arr, i, 0)
    return arr

num_list = df['numbers'].tolist()
sorted_list = heap_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Heap sort is an in-place algorithm with O(n log n) time complexity. It is not a stable sort, but its strictly bounded memory footprint makes it useful in certain system scenarios."
    }
