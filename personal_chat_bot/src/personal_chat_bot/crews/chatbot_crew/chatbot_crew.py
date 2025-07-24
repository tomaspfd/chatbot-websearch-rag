from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from crewai.agents.agent_builder.base_agent import BaseAgent
from crewai_tools import (
    SerperDevTool,
    PDFSearchTool
)
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
class ChatBotCrew:
    """ChatBotCrew"""

    agents: List[BaseAgent]
    tasks: List[Task]

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"


    
    @property
    def llm(self) -> LLM:
        """Lazily loads and caches the LLM instance based on model_config.txt"""
        if not hasattr(self, "_llm"):
            base_dir = Path(__file__).resolve().parents[4]
            config_file = base_dir / "model_config.txt"

            try:
                with open(config_file, "r") as f:
                    lines = f.read().splitlines()
                    model_source = lines[0].strip()
                    model_name = lines[1].strip()
            except Exception:
                model_source = "Local"
                model_name = "gemma3"

            if model_source == "Local":
                self._llm = LLM(
                    model=f"ollama/{model_name}",
                    base_url="http://localhost:11434"
                )
            elif model_source == "API":
                self._llm = LLM(
                    model=f"gemini/{model_name}",
                    api_key=os.getenv("GEMINI_API_KEY"),
                    temperature=0.5
                )
            else:
                raise ValueError(f"Unsupported model_source: {model_source}")

        return self._llm
        

    def create_search_tool(self):
        base_dir = Path(__file__).resolve().parents[4]
        pdf_path = base_dir / "uploaded.pdf"

        # Reconstruct the LLM config manually based on the LLM object
        config_file = base_dir / "model_config.txt"

        try:
            with open(config_file, "r") as f:
                lines = f.read().splitlines()
                model_source = lines[0].strip()
                model_name = lines[1].strip()
        except Exception:
            model_source = "API"
            model_name = "gemini-2.5-flash"

        # Build LLM config dict (not LLM instance)
        if model_source == "Local":
            llm_config = {
                "provider": "ollama",
                "config": {
                    "model": model_name,
                    "base_url": "http://localhost:11434"
                }
            }
        elif model_source == "API":
            llm_config = {
                "provider": "google",
                "config": {
                    "model": model_name,
                    "api_key": os.getenv("GEMINI_API_KEY"),
                    "base_url": "https://api.gemini.google.com/v1",
                    "temperature": 0.0
                }
            }
        else:
            raise ValueError(f"Unsupported model_source: {model_source}")

        pdf_search_tool = PDFSearchTool(
            pdf=pdf_path,
            config=dict(
                llm=llm_config,
                embedder=dict(
                    provider="ollama",
                    config=dict(
                        model="nomic-embed-text"
                    )
                )
            )
        )
        return pdf_search_tool

    

    def create_tool_list(self):
        base_dir = Path(__file__).resolve().parents[4]
        config_file = base_dir / "tool_config.txt"
        tools = []
        try:
            with open(config_file, "r") as f:
                tool = f.read().strip()
        except FileNotFoundError:
            return tools

        if tool == "Web Search":
            tools.append(SerperDevTool())
        elif tool == "RAG":
            tools.append(self.create_search_tool())

        return tools
        

    # If you would lik to add tools to your crew, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def chatbot(self) -> Agent:
        tools = self.create_tool_list()
        print(f"\n\n\n\n\n\n\n\n\nUsing tools: {tools} (here)\n\n\n\n\n\n\n\n")
        return Agent(
            config=self.agents_config["chatbot"],  # type: ignore[index]
            verbose=False,
            llm=self.llm,
            tools=tools,
            #memory=True
        )


    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def reply_to_user(self) -> Task:
        return Task(
            config=self.tasks_config["reply_to_user"],  # type: ignore[index]
        )
    

    @crew
    def crew(self) -> Crew:
        """Creates the ChatBot Crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents,  # Automatically created by the @agent decorator
            tasks=self.tasks,  # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True
        )
