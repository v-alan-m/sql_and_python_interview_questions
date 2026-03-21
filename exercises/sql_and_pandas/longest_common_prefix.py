import pandas as pd

def get_exercise():
    return {
        "title": "Longest Common Prefix",
        "description": "Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string.",
        "data": pd.DataFrame({
            "group_id": [1, 1, 1, 2, 2, 2],
            "string": ["flower", "flow", "flight", "dog", "racecar", "car"]
        }),
        "table_name": "string_groups",
        "allowed_modes": ["SQL", "Python"],
        "hint_python": "Group by the ID. For each group, take the first string as a reference prefix. Iterate through its characters and check if the other strings in the group match at that position.",
        "hint_sql": "SQL isn't naturally great at dynamic substring matching across rows like this without complex recursive CTEs, but you can use string functions like `LEFT()` and standard aggregation if the prefix length is known or bounded.",
        "solution_python": """
def get_longest_prefix(strings):
    strings = list(strings)
    if not strings:
        return ""
    
    # Sort strings to easily compare the most different strings first
    strings = sorted(strings)
    first = strings[0]
    last = strings[-1]
    
    prefix = []
    # Compare first and last string since they will differ the most
    for i in range(min(len(first), len(last))):
        if first[i] == last[i]:
            prefix.append(first[i])
        else:
            break
            
    return "".join(prefix)

# Group by ID and apply the prefix function
result = df.groupby("group_id")["string"].apply(get_longest_prefix).reset_index()
result.rename(columns={"string": "longest_prefix"}, inplace=True)
""",
        "solution_sql": """\
-- Getting true longest common prefix in pure SQL across arbitrary rows is complex.
-- It typically requires a Numbers/Tally table or a Recursive CTE to iterate character by character.
-- Here is a robust recursive CTE approach using a Numbers CTE:

WITH RECURSIVE Numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM Numbers WHERE n < 100
),
PrefixCheck AS (
    SELECT 
        sg.group_id,
        num.n,
        MIN(LEFT(sg.string, num.n)) as prefix,
        COUNT(DISTINCT LEFT(sg.string, num.n)) as distinct_count,
        COUNT(sg.string) as total_count,
        (SELECT COUNT(*) FROM string_groups WHERE group_id = sg.group_id) as group_size
    FROM string_groups sg
    JOIN Numbers num ON num.n <= LENGTH(sg.string) OR LENGTH(sg.string) = 0
    GROUP BY sg.group_id, num.n
)
SELECT 
    g.group_id,
    COALESCE(MAX(CASE WHEN pc.distinct_count = 1 AND pc.total_count = g.group_size THEN pc.prefix ELSE '' END), '') as longest_prefix
FROM (SELECT group_id, COUNT(*) as group_size FROM string_groups GROUP BY group_id) g
LEFT JOIN PrefixCheck pc ON g.group_id = pc.group_id
GROUP BY g.group_id
ORDER BY g.group_id;
""",
        "deep_dive": "In Pandas/Python, sorting the array of strings first takes O(N log N * M) time where M is max string length. But it simplifies the problem to only comparing the bounds (first and last strings), making the final check O(M). Total time is dominated by the sort. Pure SQL struggles with this problem type because SQL sets are inherently unordered and string manipulation across sets isn't a native paradigm like aggregations are.",
        
        # --- MULTI-STAGE INTERVIEW DATA ---
        "interview_stages": [
            {
                "stage_number": 1,
                "title": "Identical Strings",
                "scenario": "The easiest base case. All strings within a group are exactly the same. We just need to find that string.",
                "hint": "Use a simple `.first()`, `.max()`, or `MIN()` aggregation per group.",
                "data": pd.DataFrame({
                    "group_id": [1, 1, 2, 2, 2],
                    "string": ["car", "car", "banana", "banana", "banana"]
                }),
                "evaluation_criteria": [
                    "Basic grouping and aggregations.",
                    "Handling group-level operations without loops."
                ],
                "solution_code": """\
result = df.groupby('group_id')['string'].first().reset_index()
result.rename(columns={'string': 'longest_prefix'}, inplace=True)
""",
                "solution_sql": """\
SELECT group_id, MIN(string) as longest_prefix
FROM string_groups
GROUP BY group_id
ORDER BY group_id;
""",
                "expected_output": pd.DataFrame({
                    "group_id": [1, 2],
                    "longest_prefix": ["car", "banana"]
                }),
                "follow_up_probes": [
                    "Why did you use `first()` vs `max()`? Does one have a performance benefit?"
                ]
            },
            {
                "stage_number": 2,
                "title": "Single-Character Common Prefix Check",
                "scenario": "Strings might differ now. Let's build up to the solution: check if they at least share the very first character. If they do, return that character; otherwise, return an empty string. Let's assume there are no empty strings in this dataset.",
                "hint": "You can extract just the first character. If the minimum first character equals the maximum in the group, they all share it.",
                "data": pd.DataFrame({
                    "group_id": [1, 1, 1, 2, 2, 3, 3],
                    "string": ["apple", "apricot", "ape", "dog", "cat", "banana", "boat"]
                }),
                "evaluation_criteria": [
                    "String indexing and substring functions.",
                    "Conditional logic checking sets of data."
                ],
                "solution_code": """\
def check_first(strings):
    first_char = strings.iloc[0][0]
    for s in strings:
        if s[0] != first_char:
            return ""
    return first_char

result = df.groupby("group_id")["string"].apply(check_first).reset_index(name="longest_prefix")
""",
                "solution_sql": """\
SELECT group_id, 
       CASE WHEN MIN(SUBSTRING(string, 1, 1)) = MAX(SUBSTRING(string, 1, 1)) 
            THEN MIN(SUBSTRING(string, 1, 1)) 
            ELSE '' END as longest_prefix
FROM string_groups
GROUP BY group_id
ORDER BY group_id;
""",
                "expected_output": pd.DataFrame({
                    "group_id": [1, 2, 3],
                    "longest_prefix": ["a", "", "b"]
                }),
                "follow_up_probes": [
                    "Is an explicit loop needed in Python here, or could you use Series operations?",
                    "What are the edge cases with `SUBSTRING` or indexing if strings are empty?"
                ]
            },
            {
                "stage_number": 3,
                "title": "Bounded Prefix Length (Max 5)",
                "scenario": "What if you're not allowed to use recursion or complex iteration, but you are guaranteed the maximum string length across all datasets will never exceed 5 characters? Write a solution that checks prefixes up to length 5.",
                "hint": "You can use a bounded loop from 5 down to 1 in Python. In SQL, you can use a sequential `CASE` statement checking prefixes of length 5, then 4, etc.",
                "data": pd.DataFrame({
                    "group_id": [1, 1, 1, 2, 2, 2, 3, 3, 4, 4],
                    "string": ["flower", "flow", "flight", "dog", "racecar", "car", "apple", "apple", "smart", "smash"]
                }),
                "evaluation_criteria": [
                    "Understanding prefix evaluation progressively.",
                    "Brute-force logic when lengths are bounded."
                ],
                "solution_code": """\
def bounded_prefix(strings):
    strings = list(strings)
    for i in range(5, 0, -1):
        prefixes = {s[:i] for s in strings}
        if len(prefixes) == 1:
            return list(prefixes)[0]
    return ""

result = df.groupby("group_id")["string"].apply(bounded_prefix).reset_index(name="longest_prefix")
""",
                "solution_sql": """\
SELECT group_id,
  CASE 
    WHEN MIN(SUBSTR(string, 1, 5)) = MAX(SUBSTR(string, 1, 5)) THEN MIN(SUBSTR(string, 1, 5))
    WHEN MIN(SUBSTR(string, 1, 4)) = MAX(SUBSTR(string, 1, 4)) THEN MIN(SUBSTR(string, 1, 4))
    WHEN MIN(SUBSTR(string, 1, 3)) = MAX(SUBSTR(string, 1, 3)) THEN MIN(SUBSTR(string, 1, 3))
    WHEN MIN(SUBSTR(string, 1, 2)) = MAX(SUBSTR(string, 1, 2)) THEN MIN(SUBSTR(string, 1, 2))
    WHEN MIN(SUBSTR(string, 1, 1)) = MAX(SUBSTR(string, 1, 1)) THEN MIN(SUBSTR(string, 1, 1))
    ELSE ''
  END AS longest_prefix
FROM string_groups
GROUP BY group_id
ORDER BY group_id;
""",
                "expected_output": pd.DataFrame({
                    "group_id": [1, 2, 3, 4],
                    "longest_prefix": ["fl", "", "apple", "sma"]
                }),
                "follow_up_probes": [
                    "Why iterate backwards from 5 down to 1 instead of 1 up to 5?",
                    "What happens if a string is shorter than the substring index in Python vs SQL?"
                ]
            },
            {
                "stage_number": 4,
                "title": "Full Problem and Edge Cases",
                "scenario": "Now solve it for any dynamic string length, including proper handling of empty strings and no-matching prefixes.",
                "hint": "For Python, sorting the strings limits combinations—you only need to compare the alphabetically first and last strings! For SQL, use a Recursive CTE using a Numbers/Tally structure to increment substring length dynamically.",
                "data": pd.DataFrame({
                    "group_id": [1, 1, 1, 2, 2, 3, 3, 4, 4, 5, 5],
                    "string": [
                        "interview", "intervene", "internet",
                        "abc", "",
                        "same", "same",
                        "prefix", "prefixes",
                        "cat", "dog"
                    ]
                }),
                "evaluation_criteria": [
                    "Optimal time-complexity solutions (Python sort).",
                    "Advanced SQL recursive query logic.",
                    "Robust edge case handling (empty strings, complete mismatch)."
                ],
                "solution_code": """\
def get_longest_prefix(strings):
    strings = list(strings)
    if not strings:
        return ""
    
    strings = sorted(strings)
    first = strings[0]
    last = strings[-1]
    
    prefix = []
    for i in range(min(len(first), len(last))):
        if first[i] == last[i]:
            prefix.append(first[i])
        else:
            break
            
    return "".join(prefix)

result = df.groupby("group_id")["string"].apply(get_longest_prefix).reset_index(name="longest_prefix")
""",
                "solution_sql": """\
WITH RECURSIVE Numbers AS (
    SELECT 1 as n
    UNION ALL
    SELECT n + 1 FROM Numbers WHERE n < 100
),
PrefixCheck AS (
    SELECT 
        sg.group_id,
        num.n,
        MIN(LEFT(sg.string, num.n)) as prefix,
        COUNT(DISTINCT LEFT(sg.string, num.n)) as distinct_count,
        COUNT(sg.string) as total_count,
        (SELECT COUNT(*) FROM string_groups WHERE group_id = sg.group_id) as group_size
    FROM string_groups sg
    JOIN Numbers num ON num.n <= LENGTH(sg.string) OR LENGTH(sg.string) = 0
    GROUP BY sg.group_id, num.n
)
SELECT 
    g.group_id,
    COALESCE(MAX(CASE WHEN pc.distinct_count = 1 AND pc.total_count = g.group_size THEN pc.prefix ELSE '' END), '') as longest_prefix
FROM (SELECT group_id, COUNT(*) as group_size FROM string_groups GROUP BY group_id) g
LEFT JOIN PrefixCheck pc ON g.group_id = pc.group_id
GROUP BY g.group_id
ORDER BY g.group_id;
""",
                "expected_output": pd.DataFrame({
                    "group_id": [1, 2, 3, 4, 5],
                    "longest_prefix": ["inter", "", "same", "prefix", ""]
                }),
                "follow_up_probes": [
                    "In Python, what is the time complexity of sorting vs checking character by character?",
                    "In SQL, why do we need to compare `total_count` to the original `group_size`? (To ensure all strings actually contributed to a prefix of length n)."
                ]
            }
        ]
    }
