from pydantic import BaseModel

class CodeRequest(BaseModel):
    user_id: str = "anonymous"
    language: str
    version: str = "latest"
    task: str
    style: str = "modular"
    model: str = "llama3.2"

class TaskRequest(BaseModel):
    user_id: str
    language: str
    version: str
    style: str
    task: str
    model: str = "llama3.2"
    project_id: str | None = None
    file_path: str | None = None
    existing_code: str | None = None
    diff_snippet: str | None = None