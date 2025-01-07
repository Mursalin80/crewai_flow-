from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from icecream import ic

# from langchain_openai import ChatOpenAI
from ...types import BookOutline
from ..llm.llms import llm_groq_llama_3 as llm


@CrewBase
class OutlineCrew:
    """Book Outline Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher_for_outline(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["researcher_for_outline"],
            tools=[search_tool],
            llm=llm,
            verbose=True,
        )

    @agent
    def outliner_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["outliner_writer"],
            llm=llm,
            verbose=True,
        )

    @task
    def research_topic(self) -> Task:
        return Task(
            config=self.tasks_config["research_topic"],
        )

    @task
    def generate_outline(self) -> Task:
        return Task(
            config=self.tasks_config["generate_outline"], output_pydantic=BookOutline
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Book Outline Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
