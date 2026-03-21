import pandas as pd

def get_exercise():
    return {
        "title": "Bucket Sort (1/10)",
        "subtitle": "Loops, Arrays / Lists",
        "description": "Implement the Bucket Sort algorithm for floating point numbers in range [0, 1). You are given a DataFrame with a single column 'numbers'. Sort the numbers in ascending order and return the result as a list.",
        "data": pd.DataFrame({"numbers": [0.897, 0.565, 0.656, 0.1234, 0.665, 0.3434]}),
        "allowed_modes": ["Python"],
        "hint_python": "Distribute elements into a number of buckets. Sort these buckets individually, and then concatenate the sorted buckets.",
        "solution_python": """def bucket_sort(arr):
    if len(arr) == 0:
        return arr
        
    bucket = []
    slot_num = 10 
    for i in range(slot_num):
        bucket.append([])
        
    for j in arr:
        index_b = int(slot_num * j)
        # edge case if j == 1
        if index_b == slot_num:
             index_b -= 1
        bucket[index_b].append(j)
        
    for i in range(slot_num):
        bucket[i] = sorted(bucket[i])
        
    k = 0
    for i in range(slot_num):
        for j in range(len(bucket[i])):
            arr[k] = bucket[i][j]
            k += 1
    return arr

num_list = df['numbers'].tolist()
sorted_list = bucket_sort(num_list)
result = sorted_list
""",
        "deep_dive": "Bucket sort works best when elements are uniformly distributed over a range. Its average time complexity is O(n + k), making it very efficient for specific data distributions.",
        "big_o_explanation": "**Time Complexity:** `O(N + K)` average, `O(N^2)` worst case.\n**Space Complexity:** `O(N + K)`.\n\n**Explanation:** Bucket Sort achieves average `O(N + K)` time complexity by distributing `N` elements into `K` buckets. Assumed uniform distribution results in a constant number of items per bucket, making the individual bucket sorting step take `O(1)` time each. This is a massive optimization over `O(N log N)` algorithms specifically for uniformly distributed floating-point numbers. Space complexity is `O(N + K)` due to the supplemental bucket arrays storing all elements."
    }
