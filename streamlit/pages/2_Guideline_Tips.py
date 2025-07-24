import streamlit as st

st.set_page_config(page_title="Guideline Tips", page_icon="✍️")

st.title("✍️ Tips for Writing Agent and Task Descriptions")

st.markdown("""
Use this guide to write strong, focused agent and task configurations.  
These tips apply to the fields you edit in the **Guidelines** page.
""")

st.markdown("---")

### Agent Fields

st.subheader("👤 Agent Fields")

st.markdown("#### 🔹 `role`")
st.markdown("""
- Define **what the agent is** in one sentence.
- Be concise and specific.
- Avoid vague terms like "helper" or "AI thing."

**Examples:**
- ✅ `"Financial Analyst specializing in venture capital trends"`
- ✅ `"Senior Python Developer skilled in debugging legacy systems"`
""")

st.markdown("#### 🔹 `goal`")
st.markdown("""
- Describe **what the agent wants to achieve**.
- Keep it actionable and outcome-driven.

**Examples:**
- ✅ `"Identify promising startup investment opportunities based on market data"`
- ✅ `"Explain technical concepts to non-experts clearly and simply"`
""")

st.markdown("#### 🔹 `backstory`")
st.markdown("""
- Give the agent **personality and context**. This helps it act more naturally.
- Mention domain expertise, origin, or purpose.

**Examples:**
- ✅ `"An AI trained on thousands of case studies to help entrepreneurs succeed"`
- ✅ `"A chatbot created by a team of neuroscientists to answer brain-related questions"`
""")

st.markdown("---")

### Task Fields

st.subheader("🧾 Task Fields")

st.markdown("#### 🔸 `description`")
st.markdown("""
- Write **what the agent should do** in this task.
- Be imperative and clear — think of this like a command.

**Examples:**
- ✅ `"Analyze the user's message and extract the main concern"`
- ✅ `"Generate a follow-up question to guide the conversation"`
""")

st.markdown("#### 🔸 `expected_output`")
st.markdown("""
- Define **what kind of response is expected**, and optionally, its format.
- Be specific about structure, tone, or limits.

**Examples:**
- ✅ `"A concise answer no longer than 3 sentences"`
- ✅ `"A markdown-formatted list of pros and cons"`
- ✅ `"An empathetic paragraph that acknowledges the user's emotions"`

❗ Pro tip: If you want code, say so! E.g., `"A Python function to scrape titles from a web page"`
""")

st.markdown("---")

st.success("📌 Keep all inputs short, specific, and focused on the task. Use plain English and avoid fluff!")

st.markdown("Feel free to go back to the **Guidelines** page to adjust your inputs using these tips.")
