import pandas as pd

def get_exercise():
    return {
        "title": "Quick Sort (3/10)",
        "subtitle": "Loops, Arrays / Lists",
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
        "deep_dive": "Quick sort has an average time complexity of O(n log n) and is very fast in practice due to contiguous memory access. Its worst-case is O(n^2), usually avoided with good pivot selection.",
        "big_o_explanation": "**Time Complexity:** `O(N log N)` average, `O(N^2)` worst case.\n**Space Complexity:** `O(N)` auxiliary space for this specific implementation.\n\n**Explanation:** Quick Sort efficiently divides elements into smaller and larger subarrays in `O(N)` time around a pivot. The average depth of the recursive tree is `O(log N)`, yielding an overall `O(N log N)` average time complexity, which optimizes the `O(N^2)` bound of naive sorts. However, this specific Python implementation creates new lists for `left`, `middle`, and `right` partitions at each step, resulting in `O(N)` space. An in-place implementation would optimize space to `O(log N)`."
    }
