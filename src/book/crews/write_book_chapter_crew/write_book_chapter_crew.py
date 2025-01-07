from crewai import LLM, Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool

from ...types import Chapter
from ..llm.llms import llm_google_gemini as llm


@CrewBase
class WriteBookChapterCrew:
    """Write Book Chapter Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def researcher_for_book_chapter(self) -> Agent:
        search_tool = SerperDevTool()
        return Agent(
            config=self.agents_config["researcher_for_book_chapter"],
            tools=[search_tool],
            llm=llm,
            verbose=True,
        )

    @agent
    def writer_for_book_chapter(self) -> Agent:
        return Agent(
            config=self.agents_config["writer_for_book_chapter"],
            llm=llm,
            verbose=True,
        )

    @task
    def research_chapter(self) -> Task:
        return Task(
            config=self.tasks_config["research_chapter"],
        )

    @task
    def write_chapter(self) -> Task:
        return Task(config=self.tasks_config["write_chapter"], output_pydantic=Chapter)

    @crew
    def crew(self) -> Crew:
        """Creates the Write Book Chapter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
