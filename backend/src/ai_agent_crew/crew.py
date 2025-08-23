from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from crewai_tools import SerperDevTool, PDFSearchTool, ScrapeWebsiteTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class AiAgentCrew():
    """AiAgentCrew crew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    
    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def market_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['market_researcher'], # type: ignore[index]
            tools=[SerperDevTool(), PDFSearchTool(), ScrapeWebsiteTool()],
            verbose=True
        )

    @agent
    def prospecting_specialist(self) -> Agent:
        return Agent(
            config=self.agents_config['prospecting_specialist'], # type: ignore[index]
            verbose=True
        )

    @agent
    def content_writer(self) -> Agent:
        return Agent(
            config=self.agents_config['content_writer'], # type: ignore[index]
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def prospect_identification_task(self) -> Task:
        return Task(
            config=self.tasks_config['prospect_identification_task'], # type: ignore[index]
            agent=self.market_researcher()
        )

    @task
    def prospecting_email_task(self) -> Task:
        return Task(
            config=self.tasks_config['prospecting_email_task'], # type: ignore[index]
            agent=self.prospecting_specialist()
        )

    @task
    def prospecting_report_task(self) -> Task:
        return Task(
            config=self.tasks_config['prospecting_report_task'], # type: ignore[index]
            agent=self.content_writer(),
            output_file='report.md'
        )

    @crew
    def crew(self) -> Crew:
        """Creates the AiAgentCrew crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
