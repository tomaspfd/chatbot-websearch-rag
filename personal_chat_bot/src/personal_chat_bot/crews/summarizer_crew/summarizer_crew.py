from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from typing import List
from dotenv import load_dotenv
from pydantic import Field
import os
from pathlib import Path

load_dotenv()
# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators


@CrewBase
class SummarizerCrew:
    """SummarizerCrew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @property
    def llm(self) -> LLM:
        base_dir = Path(__file__).resolve().parents[4]
        config_file = base_dir / "model_config.txt"

        try:
            with open(config_file, "r") as f:
                lines = f.read().splitlines()
                model_source = lines[0].strip()
                model_name = lines[1].strip()
        except Exception as e:
            model_source = "Local"
            model_name = "gemma3"

        if model_source == "Local":
            return LLM(model= f"ollama/{model_name}", base_url="http://localhost:11434")
        elif model_source == "API":
            return LLM(model=f"gemini/{model_name}", api_key=os.getenv("GEMINI_API_KEY"), temperature=0.7)
        else:
            raise ValueError(f"Unsupported model_source: {model_source}")

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools

    @agent
    def chat_summarizer(self) -> Agent:
        return Agent(
            config=self.agents_config["chat_summarizer"],  # type: ignore[index]
            verbose=False,
            llm=self.llm,
            #memory=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    
    @task
    def summarize_chat(self) -> Task:
        return Task(
            config=self.tasks_config["summarize_chat"],  # type: ignore[index]
        )

    @crew
    def crew(self) -> Crew:
        """Creates the Summarizer Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
