import streamlit as st
import yaml
from pathlib import Path

# === File paths ===
BASE_DIR = Path(__file__).resolve().parent.parent.parent
CONFIG_DIR = BASE_DIR / "personal_chat_bot" / "src" / "personal_chat_bot" / "crews" / "chatbot_crew" / "config"

AGENTS_PATH = CONFIG_DIR / "agents.yaml"
TASKS_PATH = CONFIG_DIR / "tasks.yaml"

AGENT_KEY = "chatbot"
TASK_KEY = "reply_to_user"

# === Load existing YAMLs ===
default_agent = {}
default_task = {}

if AGENTS_PATH.exists():
    with open(AGENTS_PATH, "r") as f:
        agents_data = yaml.safe_load(f) or {}
        default_agent = agents_data.get(AGENT_KEY, {})

if TASKS_PATH.exists():
    with open(TASKS_PATH, "r") as f:
        tasks_data = yaml.safe_load(f) or {}
        default_task = tasks_data.get(TASK_KEY, {})

# === UI: Agent ===
st.title("🛠️ Configure Your Agent and Task")
st.header("Agent Configuration")

role = st.text_area("Role", value=default_agent.get("role", ""))
goal = st.text_area("Goal", value=default_agent.get("goal", ""))
backstory = st.text_area("Backstory", value=default_agent.get("backstory", ""))

# === UI: Task ===
st.header("Task Configuration")

description = st.text_area("Description", value=default_task.get("description", ""))
expected_output = st.text_area("Expected Output", value=default_task.get("expected_output", ""))

# === Save Button ===
if st.button("💾 Save"):
    agents_data[AGENT_KEY] = {
        "role": role,
        "goal": goal,
        "backstory": backstory
    }

    tasks_data[TASK_KEY] = {
        "description": description,
        "expected_output": expected_output,
        "agent": AGENT_KEY  # maintain agent reference
    }

    with open(AGENTS_PATH, "w") as f:
        yaml.dump(agents_data, f, sort_keys=False)

    with open(TASKS_PATH, "w") as f:
        yaml.dump(tasks_data, f, sort_keys=False)

    st.success("✅ Agent and Task updated successfully!")
