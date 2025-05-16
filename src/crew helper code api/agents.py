
from crewai import Agent, Task, Crew
from langchain.agents import tool
from llm_client import call_llm

class CodeCrew:

    def build_stateless_crew(self, request):
        planner = Agent(
            role='Planner',
            goal='Understand and refine the code generation task.',
            backstory='You help software engineers translate tasks into precise coding subtasks.',
            allow_delegation=False,
            verbose=True
        )

        coder = Agent(
            role='CodeWriter',
            goal='Write high-quality code based on task details.',
            backstory='You are a seasoned software developer with a modular coding style.',
            allow_delegation=False,
            verbose=True
        )

        planning_task = Task(
            description=f"Refine the coding task: '{request.task}' for {request.language} {request.version}.",
            expected_output="A clarified, executable version of the coding requirement.",
            agent=planner
        )

        coding_task = Task(
            description=(
                f"Write modular {request.language} code for the task: {request.task}. "
                f"Style: {request.style}. Output only code."
            ),
            expected_output="A complete code snippet.",
            agent=coder
        )

        crew = Crew(
            agents=[planner, coder],
            tasks=[planning_task, coding_task],
            verbose=True
        )
        return crew

    def build_diff_crew(self, request):
        planner = Agent(
            role='UpdatePlanner',
            goal='Understand how the code should be updated based on the diff.',
            backstory='You help engineers interpret update snippets and existing code changes.',
            allow_delegation=False,
            verbose=True
        )

        coder = Agent(
            role='CodeUpdater',
            goal='Apply changes to existing code accurately.',
            backstory='You are an expert at refactoring and updating code cleanly.',
            allow_delegation=False,
            verbose=True
        )

        analyze_task = Task(
            description=(
                f"Understand the update to be made in this {request.language} file."
                f"File path: {request.file_path}"
                f"Existing code:{request.existing_code}"
                f"Update snippet:{request.diff_snippet}"
            ),
            expected_output="Summary of changes to be made.",
            agent=planner
        )

        update_task = Task(
            description=(
                f"Apply the update snippet to the given code and return the updated {request.language} code. "
                f"Style: {request.style}. Respond only with the final code."
            ),
            expected_output="Updated code block only.",
            agent=coder
        )

        crew = Crew(
            agents=[planner, coder],
            tasks=[analyze_task, update_task],
            verbose=True
        )
        return crew
