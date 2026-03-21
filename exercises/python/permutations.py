import pandas as pd

def get_exercise():
    return {
        "title": "Permutations",
        "subtitle": "Recursion, Loops, Arrays / Lists, Sets",
        "description": "Given a string, print or return a list of all its valid permutations. You can assume all characters in the string are unique.",
        "data": pd.DataFrame({
            "string": ["abc", "ab", "a"]
        }),
        "allowed_modes": ["Python"],
        "hint_python": "You can use recursion. The base case is when the string is length 1. Otherwise, for each character in the string, extract it and recursively find permutations of the remaining characters, then prepend the extracted character. Alternatively, use `itertools.permutations`.",
        "hint_sql": "Not applicable",
        "solution_python": """
import itertools

def get_permutations(s):
    # Using itertools logic (Optimal for Python)
    # permutations returns tuples of characters, so we join them
    perms = itertools.permutations(s)
    return ["".join(p) for p in perms]

    # Recursive approach (good to know for interviews):
    # if len(s) <= 1:
    #     return [s]
    # result = []
    # for i, char in enumerate(s):
    #     remaining = s[:i] + s[i+1:]
    #     for p in get_permutations(remaining):
    #         result.append(char + p)
    # return result

df["permutations"] = df["string"].apply(get_permutations)
result = df
""",
        "solution_sql": "Not applicable",
        "deep_dive": "Generating permutations is computationally heavy. For a string of length N, there are N! (N factorial) permutations. Therefore, both the time and space complexity are O(N * N!), as we must generate N! combinations and each combination takes O(N) space. `itertools.permutations` is implemented in C and is significantly faster than purely manual recursive approaches in Python.",
        "big_o_explanation": "Time Complexity: O(N * N!) where N is the length of the string. There are N! permutations, and creating each permutation (joining the characters) takes O(N) time. Space Complexity: O(N * N!) to store all the generated permutations in the final list. Using Python's built-in `itertools.permutations` is highly optimized in C and avoids the overhead of manual recursion.",
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Unique Characters",
                "scenario": "Implement a function to return a list of all valid permutations of a string. You can assume all characters in the string are unique, and you should output the permutations in a deterministic (sorted) order. Using built-in combinations libraries is allowed for this first step.",
                "hint": "You can use `itertools.permutations`. Alternatively, you can use recursion by picking one character at a time and permuting the remainder of the string.",
                "data": pd.DataFrame({
                    "string": ["abc", "ab", "a"]
                }),
                "evaluation_criteria": [
                    "Understanding of combinatorial generation.",
                    "Correct use of standard library tools or recursive approach.",
                    "Correct formatting of the output (list of strings)."
                ],
                "solution_code": """\
import itertools

def get_permutations(s):
    # Using standard library
    perms = itertools.permutations(s)
    # Join the tuples and sort to ensure deterministic deterministic order
    return sorted(["".join(p) for p in perms])

df["permutations"] = df["string"].apply(get_permutations)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "ab", "a"],
                    "permutations": [
                        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'],
                        ['ab', 'ba'],
                        ['a']
                    ]
                }),
                "big_o_explanation": "Time Complexity: O(N * N!) to generate and join all permutations, plus O((N!) log(N!)) to sort them lexicographically. Space Complexity: O(N * N!) to store the resulting list of strings. Providing a deterministic (sorted) output increases the time complexity but does not increase the overall space bound.",
                "follow_up_probes": [
                    "Time Complexity: What is the time and space complexity of generating all permutations?",
                    "Alternative approach: If `itertools` was not available, how would you implement this recursively?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Duplicate Characters",
                "scenario": "Now assume the input string can contain duplicate characters (e.g., 'aba'). Your function should still return all **unique** permutations of the string, sorted alphabetically.",
                "hint": "Generating permutations for a string with identical characters will produce duplicates. Consider using a `set` to collect the permutations before returning them as a sorted list.",
                "data": pd.DataFrame({
                    "string": ["abc", "aba", "aa"]
                }),
                "evaluation_criteria": [
                    "Ability to handle state across iterations/recursions.",
                    "Knowledge of Data Structures (using Sets for fast deduplication).",
                    "Edge case handling for fully identical strings (like 'aa')."
                ],
                "solution_code": """\
import itertools

def get_permutations(s):
    # Use a set comprehension to automatically deduplicate
    perms = set(["".join(p) for p in itertools.permutations(s)])
    return sorted(list(perms))

df["permutations"] = df["string"].apply(get_permutations)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "aba", "aa"],
                    "permutations": [
                        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'],
                        ['aab', 'aba', 'baa'],
                        ['aa']
                    ]
                }),
                "big_o_explanation": "Time Complexity: O(N * N!) to generate all permutations, even the duplicate ones. Sorting the unique permutations takes time proportional to the number of unique variations. Space Complexity: O(N * N!) because `itertools.permutations` still generates all combinations in memory, and the `set` stores the unique ones. Generating duplicates and filtering them is computationally wasteful compared to a backtracking algorithm that skips duplicates at generation time.",
                "follow_up_probes": [
                    "Optimisation: Removing duplicates using a set works, but it generates all N! permutations first. How could you avoid generating the duplicates entirely during the recursive step?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Filtering Adjacent Characters",
                "scenario": "Let's add a custom constraint. We only want to keep permutations where **no two adjacent characters are identical**. Filter the unique permutations to remove any that have identical characters sitting next to each other.",
                "hint": "After generating your unique permutations, iterate through the list. For each permutation, loop through its characters and check if `p[i] == p[i+1]`. Only keep those where this is never true.",
                "data": pd.DataFrame({
                    "string": ["abc", "aba", "aa", "mmo"]
                }),
                "evaluation_criteria": [
                    "Conditional iteration patterns (looping and evaluating rules over strings).",
                    "Correct boolean flag usage / early stopping when an adjacent duplicate is found."
                ],
                "solution_code": """\
import itertools

def get_permutations(s):
    perms = set(["".join(p) for p in itertools.permutations(s)])
    
    valid_perms = []
    for p in sorted(list(perms)):
        has_adjacent = False
        for i in range(len(p) - 1):
            if p[i] == p[i+1]:
                has_adjacent = True
                break
        
        if not has_adjacent:
            valid_perms.append(p)
            
    return valid_perms

df["permutations"] = df["string"].apply(get_permutations)
result = df
""",
                "expected_output": pd.DataFrame({
                    "string": ["abc", "aba", "aa", "mmo"],
                    "permutations": [
                        ['abc', 'acb', 'bac', 'bca', 'cab', 'cba'],
                        ['aba'],
                        [],
                        ['mom']
                    ]
                }),
                "big_o_explanation": "Time Complexity: O(N * N!) to generate and deduplicate permutations, plus an O(N) check per unique permutation to filter out adjacent identical characters. Space Complexity: O(N * N!) for initially storing all combinations before filtering. The naive 'generate then filter' approach is easy to write but highly inefficient; a backtracking algorithm that never generating invalid branches (early pruning) would be far more optimal.",
                "follow_up_probes": [
                    "Regex Alternative: How could you solve the adjacency check using regular expressions instead of a loop?",
                    "Early Pruning: Instead of generating and then filtering, how could you integrate this condition directly into your recursive backtracking function?"
                ]
            }
        ]
    }
