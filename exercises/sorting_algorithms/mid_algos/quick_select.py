import pandas as pd

def get_exercise():
    return {
        "title": "Quick Select (5/10)",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Find the K-th smallest element in an unordered list 'numbers'. Instead of returning the sorted list, return the exact integer. K=3. Use Quick Select to achieve this in O(N) average time.",
        "data": pd.DataFrame({"numbers": [7, 10, 4, 3, 20, 15]}),
        "allowed_modes": ["Python"],
        "hint_python": "Quick Select uses the partition logic from Quick Sort. Instead of recursing into both halves of the array, only recurse into the half that contains the K-th index.",
        "solution_python": """def partition(arr, l, r):
    x = arr[r]
    i = l
    for j in range(l, r):
        if arr[j] <= x:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[r] = arr[r], arr[i]
    return i

def quick_select(arr, l, r, k):
    if (k > 0 and k <= r - l + 1):
        index = partition(arr, l, r)

        if (index - l == k - 1):
            return arr[index]

        if (index - l > k - 1):
            return quick_select(arr, l, index - 1, k)

        return quick_select(arr, index + 1, r, k - index + l - 1)
        
    return None

num_list = df['numbers'].tolist()
# Looking for the 3rd smallest element
k_value = 3
kth_element = quick_select(num_list, 0, len(num_list) - 1, k_value)
result = kth_element
""",
        "deep_dive": "Quick Select relies on Lomuto partition scheme. It is extremely useful in big data for finding medians and percentiles because we only do work on ONE side of the pivot, dropping our average time complexity down to O(N) instead of O(N log N) sorting.",
        "big_o_explanation": "**Time Complexity:** `O(N)` average, `O(N^2)` worst case.\n**Space Complexity:** `O(log N)` average.\n\n**Explanation:** Quick Select optimizes finding the K-th element compared to a naive `O(N log N)` full sort by only recursing into the partition that contains the target index. It partitions the array using a pivot in `O(N)` time. On average, the partition splits the data in half, leading to a recurrence relation of `T(N) = T(N/2) + O(N)`, which resolves to `O(N)` average time. Space complexity is `O(log N)` due to the recursive call stack on average."
    }
