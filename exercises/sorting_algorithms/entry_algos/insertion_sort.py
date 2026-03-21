import pandas as pd

def get_exercise():
    return {
        "title": "Insertion Sort (1/10)",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Implement the Insertion Sort algorithm. You are given a DataFrame with a single column 'numbers'. Sort the numbers in ascending order and return the result as a list.",
        "data": pd.DataFrame({"numbers": [12, 11, 13, 5, 6]}),
        "allowed_modes": ["Python"],
        "hint_python": "Build the final sorted array one item at a time by taking elements from the unsorted part and inserting them into their correct position in the sorted part.",
        "solution_python": """def insertion_sort(arr):
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr

num_list = df['numbers'].tolist()
sorted_list = insertion_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Insertion sort is highly efficient for small data sets or partially sorted arrays, with an adaptive time complexity of O(n) in the best case."
    }
