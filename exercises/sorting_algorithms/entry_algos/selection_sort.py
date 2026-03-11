import pandas as pd

def get_exercise():
    return {
        "title": "Selection Sort (1/10)",
        "description": "Implement the Selection Sort algorithm. You are given a DataFrame with a single column 'numbers'. Sort the numbers in ascending order and specify the return value as a list.",
        "data": pd.DataFrame({"numbers": [29, 10, 14, 37, 14, 2, 7, 22]}),
        "allowed_modes": ["Python"],
        "hint_python": "Find the minimum element in the unsorted portion of the array and swap it with the first element of the unsorted portion.",
        "solution_python": """def selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i+1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr

num_list = df['numbers'].tolist()
sorted_list = selection_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Selection sort has an O(n^2) time complexity in all cases. It performs well on small lists and makes exactly O(n) swaps."
    }
