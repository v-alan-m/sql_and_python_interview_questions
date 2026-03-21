import pandas as pd

def get_exercise():
    return {
        "title": "Bubble Sort (1/10)",
        "subtitle": "Loops, Arrays / Lists",
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
        "big_o_explanation": "### Time Complexity: $O(N^2)$\nWhere **$N$** is the number of elements in the array.\n- The algorithm uses nested loops. The outer loop runs $N$ times, and the inner loop runs roughly $N - i$ times.\n- For each pair, it performs a comparison and potentially a swap, which takes $O(1)$ time.\n- Total comparisons roughly equal $N \\times (N-1) / 2$, which scales non-linearly to $O(N^2)$.\n- The best-case scenario (if the array is already sorted and an early termination flag is implemented) is $O(N)$, but the standard implementation consistently hits $O(N^2)$ regardless of initial state.\n\n### Space Complexity: $O(1)$\n- Bubble Sort is an **in-place** sorting algorithm.\n- It only requires a nominal amount of extra memory for temporary variables during the swapping process. It modifies the original array directly without allocating secondary arrays.\n\n### Optimization Context\nBubble Sort is fundamentally considered an inefficient algorithm for large datasets; it is primarily used as an educational entry point to computer science logic. Its main optimization benefit is its $O(1)$ space complexity. However, practically every production system uses algorithms with $O(N \\log N)$ time complexity (like Quick Sort, Merge Sort, or Timsort) because processing power scales roughly exponentially worse with $O(N^2)$ algorithms as datasets grow."
    }
