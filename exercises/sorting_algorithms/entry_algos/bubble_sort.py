import pandas as pd

def get_exercise():
    return {
        "title": "Bubble Sort (1/10)",
        "description": "Implement the Bubble Sort algorithm. You are given a DataFrame with a single column 'numbers' containing unsorted integers. Sort the list in ascending order and return a new list.",
        "data": pd.DataFrame({"numbers": [64, 34, 25, 12, 22, 11, 90]}),
        "allowed_modes": ["Python"],
        "hint_python": "Iterate through the list, comparing adjacent elements and swapping them if they are in the wrong order. Repeat until the list is sorted.",
        "solution_python": """def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n-i-1):
            if arr[j] > arr[j+1]:
                arr[j], arr[j+1] = arr[j+1], arr[j]
    return arr

# Extract list from dataframe
num_list = df['numbers'].tolist()
sorted_list = bubble_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Bubble sort has O(n^2) time complexity, making it inefficient for large datasets. However, it's easy to understand and implement.",
    }
