import pandas as pd

def get_exercise():
    return {
        "title": "Top K Elements Priority Queue (9/10)",
        "subtitle": "Queues / Priority Queues, Loops, Arrays / Lists",
        "description": "Given a large, unsorted stream of user login attempts (represented as a DataFrame column 'login_counts'), write a function to find the top K most active users without completely sorting the list. Return the result as a sorted descending list. Let K = 3.",
        "data": pd.DataFrame({"login_counts": [2, 11, 4, 18, 9, 3, 21, 14, 1, 7]}),
        "allowed_modes": ["Python"],
        "hint_python": "Use Python's built-in `heapq` module. Maintain a min-heap of size K. If a new element is larger than the root of the min-heap, pop the root and push the new element.",
        "solution_python": """import heapq

def top_k_elements(arr, k):
    # Maintain a min-heap of size K
    min_heap = []
    
    for num in arr:
        heapq.heappush(min_heap, num)
        if len(min_heap) > k:
            heapq.heappop(min_heap)
            
    # The min-heap contains the top K elements, but in ascending/heap order.
    # To return descending (most active first), sort backward:
    return sorted(min_heap, reverse=True)

counts = df['login_counts'].tolist()
result = top_k_elements(counts, 3)
""",
        "deep_dive": "This is a quintessential Data Engineering problem. Finding the Top K elements using a Min-Heap of size K takes O(N * log K) time and O(K) space, heavily outperforming sorting the entire array first (which would be O(N log N)). It allows you to process infinite data streams efficiently.",
        "big_o_explanation": "### Time Complexity: $O(N \\log K)$\nWhere **$N$** is the total number of elements in the array and **$K$** is the number of top elements we want to find.\n- For each of the $N$ elements, we push it onto the heap.\n- If the heap exceeds size $K$, we pop the smallest element. Both push and pop operations on a heap of size $K$ take $O(\\log K)$ time.\n- Doing this for all $N$ elements results in a time complexity of $O(N \\log K)$.\n- The final sort of the $K$ elements takes $O(K \\log K)$ time, but since $K \\le N$, this is dominated by $O(N \\log K)$.\n\n### Space Complexity: $O(K)$\n- The min-heap stores exactly $K$ elements at any given time.\n- Therefore, the auxiliary space used is $O(K)$, which is highly efficient compared to loading the entire dataset into memory.\n\n### Optimization Context\nA naive solution would be to sort the entire array and then slice the last $K$ elements. Sorting takes $O(N \\log N)$ time and $O(N)$ space. By using a Min-Heap of fixed size $K$, we drastically reduce both bounds. For instance, if you process 1 billion login attempts to find the top 100, $O(N \\log K)$ runs extremely fast and uses virtually no memory, whereas $O(N \\log N)$ would be computationally massive and require loading 1 billion integers into memory."
    }
