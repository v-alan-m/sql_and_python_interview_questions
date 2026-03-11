import pandas as pd

def get_exercise():
    return {
        "title": "Iterative Merge Sort (5/10)",
        "description": "Implement the Merge Sort algorithm ITERATIVELY (without recursion) to prevent call stack issues on massive datasets. You are given a DataFrame with a single column 'numbers'. Sort and return the result as a list.",
        "data": pd.DataFrame({"numbers": [4, 2, 3, 1, 6, 5]}),
        "allowed_modes": ["Python"],
        "hint_python": "Start by merging sub-arrays of size 1 to create sorted sub-arrays of size 2. Then merge those to create size 4, and so on until the entire array is sorted.",
        "solution_python": """def iterative_merge_sort(arr):
    current_size = 1
    
    # Outer loop for traversing each sub array of current_size
    while current_size < len(arr) - 1:
        left = 0
        # Inner loop for merge call in a sub array
        while left < len(arr)-1:
            # mid index = left index of sub array + current sub array size - 1
            mid = min((left + current_size - 1), (len(arr)-1))
            
            # (False if this is the last element
            # and no partner exists for merge)
            # right index = mid + current_size
            right = ((2 * current_size + left - 1, len(arr) - 1)[2 * current_size + left - 1 > len(arr)-1])
            
            # Merge call for each sub array
            # Logic for merge is identical to recursive version
            n1 = mid - left + 1
            n2 = right - mid
            L = [0] * n1
            R = [0] * n2
            
            for i in range(0, n1):
                L[i] = arr[left + i]
            for i in range(0, n2):
                R[i] = arr[mid + 1 + i]

            i, j, k = 0, 0, left
            while i < n1 and j < n2:
                if L[i] <= R[j]:
                    arr[k] = L[i]
                    i += 1
                else:
                    arr[k] = R[j]
                    j += 1
                k += 1

            while i < n1:
                arr[k] = L[i]
                i += 1
                k += 1

            while j < n2:
                arr[k] = R[j]
                j += 1
                k += 1
            left = left + current_size*2
            
        current_size = 2 * current_size
    return arr

num_list = df['numbers'].tolist()
sorted_list = iterative_merge_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Iterative Merge Sort operates purely bottom-up. It's an important concept in DE because functional/recursive programming patterns scale poorly memory-wise (due to stack frames) when sorting billions of rows across distributed clusters."
    }
