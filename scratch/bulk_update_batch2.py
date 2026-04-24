import os
import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    new_lines = []
    for line in lines:
        # Match lines like: "data": pd.DataFrame(...)
        match = re.match(r'^(\s+)"data":\s+pd\.DataFrame\(.*\),?\s*$', line)
        if match:
            indent = match.group(1)
            new_lines.append(f'{indent}"data": None,\n')
            new_lines.append(f'{indent}"hide_data": True,\n')
        else:
            new_lines.append(line)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(new_lines)

directory = r'c:\Users\VAM\Desktop\desktop_all_files\projects\python\interview_coding_questions\sql_and_python_interview_questions\exercises\python_core\python_coding'

for filename in os.listdir(directory):
    if filename.endswith('.py'):
        process_file(os.path.join(directory, filename))
        print(f"Processed {filename}")
