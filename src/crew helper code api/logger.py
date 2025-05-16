# logger.py
import logging
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_task(user_id, project_id, mode, model, task):
    task_summary = task[:100].replace("\n", " ")
    logging.info(f"[{mode.upper()}] User: {user_id}, Project: {project_id or 'stateless'}, Model: {model}, Task: {task_summary}")

def log_error(user_id, error):
    logging.error(f"[ERROR] User: {user_id}, {error}")
