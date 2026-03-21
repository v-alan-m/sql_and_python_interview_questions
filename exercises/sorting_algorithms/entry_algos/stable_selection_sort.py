import pandas as pd

def get_exercise():
    return {
        "title": "Stable Selection Sort (3/10)",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Implement a 'Stable' Selection Sort. You are given a DataFrame listing dictionaries of `{'id': int, 'val': int}`. Sort the array so that numerical 'val's are in ascending order. However, if two 'val's are equal, their original relative 'id' order must be preserved. Return the list.",
        "data": pd.DataFrame({"records": [{"id": 1, "val": 4}, {"id": 2, "val": 4}, {"id": 3, "val": 2}]}),
        "allowed_modes": ["Python"],
        "hint_python": "Standard Selection Sort is unstable because swapping distant elements can skip over equal items. To make it stable, instead of swapping the minimum element, insert it at its correct position and shift the rest of the array elements down by one.",
        "solution_python": """def stable_selection_sort(arr):
    n = len(arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if arr[min_idx]['val'] > arr[j]['val']:
                min_idx = j
                
        # Move minimum element at current i.
        key = arr[min_idx]
        while min_idx > i:
            arr[min_idx] = arr[min_idx - 1]
            min_idx -= 1
        arr[i] = key
        
    return arr

records = df['records'].tolist()
sorted_records = stable_selection_sort(records)
result = sorted_records
""",
        "deep_dive": "Understanding 'stability' in sorting is critical. When you query a database using `ORDER BY name, age`, the query engine applies a stable sort on `name` first, and then on `age`, guaranteeing that the alphabetical order within the same ages remains intact.",
        "big_o_explanation": "### Time & Space Complexity\n\n- **Time Complexity:** **O(N²)** in all scenarios. Just like standard Selection Sort, finding the minimum takes $O(N)$ operations for each element. However, shifting the remaining array elements by one spot instead of directly swapping them *also* takes $O(N)$ time per cycle. Adding these together still results in a quadratic $O(N²)$ bound.\n- **Space Complexity:** **O(1)**. Despite the mechanical complexity of shifting elements rightwards, this is entirely conducted in-place without needing external container lists.\n\n### Optimization Context\n\nThe optimization here isn't regarding raw speed, but **data integrity**. By sacrificing the $O(1)$ fast-swap operation for a slower $O(N)$ cascade shift, we guarantee the structural coherence of duplicate records. This is foundational in SQL where chaining `ORDER BY Primary, Secondary` commands naturally expects a stable sort algorithm under the hood."
    }
