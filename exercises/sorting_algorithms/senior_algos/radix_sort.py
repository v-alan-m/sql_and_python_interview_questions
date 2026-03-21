import pandas as pd

def get_exercise():
    return {
        "title": "Radix Sort (1/10)",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Implement the Radix Sort algorithm for positive integers. You are given a DataFrame with a single column 'numbers'. Sort the numbers in ascending order and return the result as a list.",
        "data": pd.DataFrame({"numbers": [170, 45, 75, 90, 802, 24, 2, 66]}),
        "allowed_modes": ["Python"],
        "hint_python": "Sort the elements digit by digit, starting from the least significant digit to the most significant digit, typically using counting sort as a subroutine.",
        "solution_python": """def counting_sort(arr, exp1):
    n = len(arr)
    output = [0] * (n)
    count = [0] * (10)
    
    for i in range(0, n):
        index = arr[i] // exp1
        count[index % 10] += 1
        
    for i in range(1, 10):
        count[i] += count[i - 1]
        
    i = n - 1
    while i >= 0:
        index = arr[i] // exp1
        output[count[index % 10] - 1] = arr[i]
        count[index % 10] -= 1
        i -= 1
        
    for i in range(0, len(arr)):
        arr[i] = output[i]

def radix_sort(arr):
    if not arr:
        return arr
    max1 = max(arr)
    exp = 1
    while max1 / exp >= 1:
        counting_sort(arr, exp)
        exp *= 10
    return arr

num_list = df['numbers'].tolist()
sorted_list = radix_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Radix sort is a non-comparative integer sorting algorithm with O(d * (n + k)) time complexity. It can be faster than O(n log n) comparison sorts for large inputs with relatively few digits.",
        "big_o_explanation": "**Time Complexity:** `O(d * (N + b))`.\n**Space Complexity:** `O(N + b)` (where `d` is max digits, `b` is base 10).\n\n**Explanation:** Radix Sort is a non-comparative algorithm that processes numbers digit by digit. Instead of direct element comparisons (bounded at `O(N log N)`), it uses a stable subroutine like Counting Sort for each of the `d` digits, taking `O(N + b)` time per pass. This provides linear-comparable `O(N)` time when `d` is small, optimizing performance for large datasets of numbers. It requires `O(N + b)` space for output and count arrays."
    }
