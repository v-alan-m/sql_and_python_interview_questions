import pandas as pd

def get_exercise():
    return {
        "title": "Merge Sort (4/10)",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Implement the Merge Sort algorithm. You are given a DataFrame with a column 'numbers'. Sort the numbers in ascending order and return the result as a list.",
        "data": pd.DataFrame({"numbers": [38, 27, 43, 3, 9, 82, 10]}),
        "allowed_modes": ["Python"],
        "hint_python": "Divide the array into two halves, recursively sort them, and then merge the two sorted halves.",
        "solution_python": """def merge_sort(arr):
    if len(arr) > 1:
        mid = len(arr) // 2
        L = arr[:mid]
        R = arr[mid:]

        merge_sort(L)
        merge_sort(R)

        i = j = k = 0

        while i < len(L) and j < len(R):
            if L[i] < R[j]:
                arr[k] = L[i]
                i += 1
            else:
                arr[k] = R[j]
                j += 1
            k += 1

        while i < len(L):
            arr[k] = L[i]
            i += 1
            k += 1

        while j < len(R):
            arr[k] = R[j]
            j += 1
            k += 1
    return arr

num_list = df['numbers'].tolist()
sorted_list = merge_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Merge sort is a divide-and-conquer algorithm with a guaranteed time complexity of O(n log n). It is a stable sort but requires O(n) extra space.",
        "big_o_explanation": "### Time & Space Complexity\n\n- **Time Complexity:** **O(N log N)** in all cases (best, worst, average). The array is constantly bisected in half until 1-element lengths are reached (which spans $O(\\log N)$ levels). Traversing the branches to merge the components together takes $O(N)$ iterations at every nested level.\n- **Space Complexity:** **O(N)** auxiliary space. Unlike in-place algorithms (like Insertion/Selection Sort), Merge Sort mathematically requires temporary subarrays (`L` and `R`) to weave values together correctly. Additionally, the Call Stack consumes $O(\\log N)$ memory frames due to the recursive nature.\n\n### Optimization Context\n\nMerge Sort fundamentally trades memory allocation for massive efficiency gains on processing speed. It is significantly faster than quadratic $O(N²)$ operations and acts as the conceptual backbone for large-scale distributed computations in frameworks like Apache Spark (where data nodes literally map and merge sorted data)."
    }
