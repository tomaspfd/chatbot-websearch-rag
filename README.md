# 🤖 Personal ChatBot with RAG and Streamlit

This is a custom-built chatbot web interface powered by [CrewAI](https://github.com/joaomdmoura/crewai), [Streamlit](https://streamlit.io/), and configurable LLM backends. It supports tool selection (e.g., Web Search, RAG), local/remote model switching, and PDF document uploading for Retrieval-Augmented Generation (RAG).

---

## 🚀 Features

- **Plug-and-Play LLM**: Easily switch between using local models (via Ollama) or API-based models (Gemini).
- **CrewAI-Powered**: Modular agent/task structure for clean logic.
- **Memory-Fed Agent**: Agent is provided with conversation history, which includes both previous user prompts and agent responses. Once a conversation becomes too large for the agent, a separate agent summarizes the conversation history. 
- **Tool Integration**: Choose from:
  - No tools (default)
  - Web Search 
  - PDF RAG
- **Chat UI**: Streamlit frontend with the following pages:
  - ChatBot: persistent chat history and model/tool selectors, as well as a button for clearing conversation history.
  - ChatBot Guidelines: page for personalizing the agent's role, goal, and backstory, as well as the task's description and expected output.
  - Guideline Tips: includes tips for writing the chabot guidelines.
  - Prompting Tips: includes tips for how improve your prompts to obtain the most useful answers from the agent.
 


---

## 🛠️ Setup Instructions

### 1. Clone the Repository

```bash
git clone https://github.com/tomaspfd/chatbot-websearch-rag.git
cd "ChatBot with RAG"
```

### 2. Create Virtual Environment

```
conda create -n crewai_streamlit_env python=3.11
conda activate crewai_streamlit_env
pip install -r requirements.txt
```

### 3. Run the App
```
streamlit run main.py
```