import pandas as pd

def get_exercise():
    return {
        "title": "Longest Common Prefix",
        "description": "Write a function to find the longest common prefix string amongst an array of strings. If there is no common prefix, return an empty string.",
        "data": pd.DataFrame({
            "group_id": [1, 1, 1, 2, 2, 2],
            "string": ["flower", "flow", "flight", "dog", "racecar", "car"]
        }),
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
        "solution_sql": """
-- Getting true longest common prefix in pure SQL across arbitrary rows is complex.
-- It typically requires a Numbers/Tally table or a Recursive CTE to iterate character by character.
-- Here is a conceptual recursive CTE approach for Postgres/standard SQL:

WITH RECURSIVE PrefixFinder AS (
    -- Base: First character
    SELECT 
        group_id, 
        LEFT(MIN(string), 1) as prefix, 
        1 as length
    FROM table_name
    GROUP BY group_id
    
    UNION ALL
    
    -- Recursive step: increment length
    SELECT 
        t.group_id,
        LEFT(MIN(t.string), CAST(p.length + 1 AS INTEGER)),
        p.length + 1
    FROM df t
    JOIN PrefixFinder p ON t.group_id = p.group_id
    WHERE LEFT(t.string, CAST(p.length AS INTEGER)) = p.prefix
      AND p.length < (SELECT MAX(LENGTH(string)) FROM df WHERE group_id = t.group_id)
    GROUP BY t.group_id, p.length, p.prefix
    HAVING COUNT(DISTINCT LEFT(t.string, CAST(p.length + 1 AS INTEGER))) = 1
)
SELECT group_id, MAX(prefix) as longest_prefix
FROM PrefixFinder
GROUP BY group_id;
""",
        "deep_dive": "In Pandas/Python, sorting the array of strings first takes O(N log N * M) time where M is max string length. But it simplifies the problem to only comparing the bounds (first and last strings), making the final check O(M). Total time is dominated by the sort. Pure SQL struggles with this problem type because SQL sets are inherently unordered and string manipulation across sets isn't a native paradigm like aggregations are."
    }
