import pandas as pd

def get_exercise():
    return {
        "title": "Quick Sort",
        "description": "Implement the Quick Sort algorithm. You are given a DataFrame with a single column 'numbers'. Sort the numbers in ascending order and return the result as a list.",
        "data": pd.DataFrame({"numbers": [10, 7, 8, 9, 1, 5]}),
        "allowed_modes": ["Python"],
        "hint_python": "Pick a pivot element and partition the array around the pivot, placing smaller elements before it and larger after it.",
        "solution_python": """def quick_sort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quick_sort(left) + middle + quick_sort(right)

num_list = df['numbers'].tolist()
sorted_list = quick_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Quick sort has an average time complexity of O(n log n) and is very fast in practice due to contiguous memory access. Its worst-case is O(n^2), usually avoided with good pivot selection."
    }
