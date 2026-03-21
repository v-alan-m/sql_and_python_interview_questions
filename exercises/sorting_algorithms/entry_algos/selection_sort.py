import pandas as pd

def get_exercise():
    return {
        "title": "Selection Sort (1/10)",
        "subtitle": "Loops, Arrays / Lists",
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
        "deep_dive": "Selection sort has an O(n^2) time complexity in all cases. It performs well on small lists and makes exactly O(n) swaps.",
        "big_o_explanation": "### Time & Space Complexity\n\n- **Time Complexity:** **O(N²)** in all cases (best, average, worst). This is because regardless of whether the array is initially sorted or scrambled, we must scan the entire remaining unsorted portion to find the true minimum element.\n- **Space Complexity:** **O(1)**. The algorithm performs all operations directly on the input array (in-place) and only stores a tiny amount of state (the `min_idx` pointer).\n\n### Optimization Context\n\nWhile Selection Sort is inherently slow for large datasets due to its quadratic time profile, it has one major redeeming quality: it performs a maximum of **O(N)** swaps. If writing to memory is an extremely slow or costly operation in your system architecture, Selection Sort mitigates the overhead better than Bubble Sort."
    }
