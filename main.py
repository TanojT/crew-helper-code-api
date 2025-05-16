from fastapi import FastAPI
from models import CodeRequest, TaskRequest
from llm_client import call_llm, check_ollama_status
from utils import detect_mode, format_markdown
from logger import log_task, log_error
from session import SessionManager
from agents import CodeCrew

crew = CodeCrew()
app = FastAPI()
session_mgr = SessionManager()


@app.post("/generate-code-only")
async def generate_code(req: CodeRequest):
    log_task(req.user_id, None, "stateless", req.model, req.task)
    prompt = crew.build_prompt(req.language, req.version, req.task, req.style, explain=False)
    response = call_llm(prompt, model=req.model)
    return {"code": response.strip()}


@app.post("/generate-with-explanation")
async def generate_code_with_explanation(req: CodeRequest):
    prompt = (
        f"You are a code generator. Write {req.language} code for this task and explain it:{req.task}"
    )
    response = call_llm(prompt, model=req.model)
    return {"response": response.strip()}

@app.get("/health")
async def health_check():
    return {"ollama_up": check_ollama_status()}

@app.post("/run-code-task")
async def run_code_task(request: TaskRequest):
    mode = detect_mode(request)
    try:
        log_task(request.user_id, request.project_id, mode, request.model, request.task)

        if mode == "diff":
            session_mgr.save(request.user_id, request.project_id, "existing_code", request.existing_code)
            session_mgr.save(request.user_id, request.project_id, "diff_snippet", request.diff_snippet)
            crew_instance = crew.build_diff_crew(request)
        else:
            crew_instance = crew.build_stateless_crew(request)

        result = crew_instance.run()
        return {"result": format_markdown(result)}

    except Exception as e:
        log_error(request.user_id, str(e))
        return {"error": "An error occurred while processing the request."}



@app.post("/run-code-task")
async def run_code_task(request: TaskRequest):
    mode = detect_mode(request)
    try:
        log_task(request.user_id, request.project_id, mode, request.model, request.task)

        if mode == "diff":
            session_mgr.save(request.user_id, request.project_id, "existing_code", request.existing_code)
            session_mgr.save(request.user_id, request.project_id, "diff_snippet", request.diff_snippet)

            prompt = (
                f"You are updating a {request.language} {request.version} project file.\n"
                f"File: {request.file_path}\n\n"
                f"Existing code:\n{request.existing_code}\n\n"
                f"Update snippet:\n{request.diff_snippet}\n\n"
                f"Task: {request.task}. Style: {request.style}. Respond with the updated code only."
            )
        else:
            prompt = (
                f"You are a modular code assistant. "
                f"Generate clean {request.language} code for this task:\n"
                f"{request.task}"
            )

        result = call_llm(prompt, model=request.model)
        return {"result": format_markdown(result)}

    except Exception as e:
        log_error(request.user_id, str(e))
        return {"error": "An error occurred while processing the request."}