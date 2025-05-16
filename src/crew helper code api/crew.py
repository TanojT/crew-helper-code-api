from crewai import Agent, Task, Crew
from crew_helper_code_api .config import agents_config, tasks_config

code_generator = Agent(
    config=agents_config['code_generator'],
    verbose=True
)

generate_code_task = Task(
    config=tasks_config['generate_code'],
    agent=code_generator
)

crew = Crew(
    agents=[code_generator],
    tasks=[generate_code_task],
    verbose=True
)
