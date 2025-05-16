import re
from models import TaskRequest

def detect_mode(req: TaskRequest) -> str:
    if req.project_id and req.file_path and req.existing_code and req.diff_snippet:
        return "diff"
    return "stateless"

def format_markdown(text):
    match = re.search(r"```[a-z]*\n(.*?)```", text, re.DOTALL)
    return f"```java\n{match.group(1).strip()}```" if match else f"```java\n{text.strip()}```"