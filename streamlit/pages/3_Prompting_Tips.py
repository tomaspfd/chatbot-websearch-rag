import streamlit as st

st.set_page_config(page_title="Prompting Tips", page_icon="💡")

st.title("💡 Prompt Engineering Tips")
st.markdown("""
Writing better prompts helps you get better answers.  
Use these techniques to improve your experience with the chatbot.
""")

st.markdown("---")

st.subheader("🧠 1. Be Clear and Specific")
st.markdown("""
- ❌ Vague: `"Tell me about space"`  
- ✅ Clear: `"Summarize the main differences between a black hole and a neutron star in 3 bullet points"`

**Tips:**
- Include the format you want (list, paragraph, table, etc.)
- Mention any constraints: word count, tone, level of detail
""")

st.subheader("🎯 2. Add Context")
st.markdown("""
Give the AI the background it needs. More context = more relevant answers.

**Examples:**
- ✅ `"I’m writing a LinkedIn post about remote work trends. Suggest a hook to start the post."`  
- ✅ `"As a college student applying for internships, how can I write a compelling personal statement?"`
""")

st.subheader("📝 3. Specify the Output Format")
st.markdown("""
If you want a certain style, structure, or tone, say so.

**Examples:**
- ✅ `"Reply in 3 short paragraphs"`  
- ✅ `"Output in JSON format"`  
- ✅ `"Make it sound friendly but professional"`
""")

st.subheader("🔁 4. Use Iteration")
st.markdown("""
Don't expect the perfect answer right away. Try follow-up prompts like:
"Rewrite that more formally"
"Now give a shorter version"
"Explain it like I'm 5"

Use the chatbot like a **collaborator**, not a one-shot oracle.
""")

st.subheader("👩‍🔬 5. Use Roles or Personas")
st.markdown("""
Ask the AI to act from a certain perspective.

**Examples:**
- ✅ `"Act as a startup advisor. Evaluate this pitch deck."`  
- ✅ `"You're a historian. Summarize the main causes of the Cold War."`
""")

st.subheader("📦 6. Break Down Complex Tasks")
st.markdown("""
For complicated problems, ask step-by-step.

> `"First, outline the sections for a grant proposal. Then write the introduction."`

This makes the response easier to follow and more accurate.
""")

st.markdown("---")

st.success("📌 Pro Tip: More guidance = better answers. Be intentional with every word in your prompt.")

st.markdown("Return to the main chat to test these techniques!")
