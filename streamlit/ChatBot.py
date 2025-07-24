import streamlit as st
# use "streamlit run main.py" to run this file

import sys
from pathlib import Path

# Point to the `src` directory
sys.path.append(str(Path(__file__).resolve().parent.parent / "personal_chat_bot" / "src"))

# Now you can import your chatbot flow
from personal_chat_bot.main import ChatBotFlow, ChatBotState



def send_and_clear():
    user_input = st.session_state.input.strip()
    if not user_input:
        return


    # Save user message
    st.session_state.conversation_history.append({"role": "user", "content": user_input})
    st.session_state.conversation_history_full.append({"role": "user", "content": user_input})

    # Run the chatbot
    st.session_state.chatbot_flow.state.conversation_history = st.session_state.conversation_history.copy()
    st.session_state.chatbot_flow.kickoff()
    st.session_state.conversation_history = st.session_state.chatbot_flow.state.conversation_history.copy()
    st.session_state.conversation_history_full.append(
        {"role": "assistant", "content": st.session_state.conversation_history[-1]['content']}
    )

    # Clear the input box
    st.session_state.input = ""




def write_model_config_to_file(model_source: str, model_name: str):
    config_path = Path(__file__).resolve().parent.parent / "model_config.txt"
    with open(config_path, "w") as f:
        f.write(f"{model_source}\n{model_name}")


def write_tool_to_file(tool: str):
    config_path = Path(__file__).resolve().parent.parent / "tool_config.txt"
    with open(config_path, "w") as f:
        f.write(tool)







# --- Streamlit App ---

st.set_page_config(page_title="My ChatBot", page_icon="🤖")



# Inject CSS to fix input at the bottom
# Inject CSS to fix input and make chat scrollable
# Inject CSS to fix input and make chat scrollable
st.markdown("""
<style>
.chat-box {
    height: 350px;
    overflow-y: auto;
    background-color: #1e1e1e;
    padding: 1rem;
    border-radius: 10px;
    border: 1px solid #333;
    font-size: 1rem;
    color: #f0f0f0;
}
.chat-entry {
    margin-bottom: 1rem;
}
.user {
    color: #ffffff;
    font-weight: bold;
}
.assistant {
    color: #ffffff;
}

div.block-container {
    padding-left: 1rem !important;
    padding-right: 1rem !important;
    padding-top: 0rem !important;
    max-width: 100% !important;
}    

/* Remove horizontal padding around the main section */
section.main > div {
    padding-left: 0 !important;
    padding-right: 0 !important;
}
            
/* Make entire page non-scrollable */
html, body {
    overflow: hidden !important;
    height: 100%;
}
section.main {
    overflow: hidden !important;
}

body, .chat-box, .stTextArea textarea {
    font-family: 'Segoe UI', sans-serif;
    font-size: 16px;
}
            

.chat-entry.user {
    background-color: #2e2e2e;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}
.chat-entry.assistant {
    background-color: #1f2d3d;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}

 
            
</style>
""", unsafe_allow_html=True)





if "model_source" not in st.session_state:
    st.session_state.model_source = "Local"
if "selected_model" not in st.session_state:
    st.session_state.selected_model = "gemma3"


# Initializing state and flow
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
    st.session_state.conversation_history_full = []









# --- Side-by-side Layout ---
left_col, right_col = st.columns([0.5, 3.5])  # Settings left, chat right

with left_col:
    st.markdown("### Settings")
    st.selectbox("Model Source", ["Local", "API"], key="model_source")
    if st.session_state.model_source == "Local":
        st.selectbox("Local Model", ["gemma3", "llama3.2", "granite3-dense"], key="local_model")
    else:
        st.selectbox("API Model", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-flash"], key="api_model")


    if (st.session_state.model_source == "API"):
        st.markdown("### Tools")
        st.radio(
            "Select a tool to enhance your assistant",
            options=["None", "Web Search", "RAG"],
            key="selected_tool"
        )
    
    if (st.session_state.get("selected_tool") == "RAG") and (st.session_state.model_source == "API"):
        st.markdown("#### Upload PDF for RAG")
        uploaded_pdf = st.file_uploader("Choose a PDF file", type=["pdf"], key="rag_pdf")

        # Optional: save PDF for future use in chatbot_crew
        if uploaded_pdf:
            pdf_path = Path(__file__).resolve().parent.parent / "uploaded.pdf"
            with open(pdf_path, "wb") as f:
                f.write(uploaded_pdf.read())
            st.toast("PDF uploaded successfully!")

    st.markdown("### Actions")
    if st.button("🧹 Clear Chat"):
        st.session_state.conversation_history = []
        st.session_state.conversation_history_full = []
        st.toast("Chat history cleared!")  # Optional feedback


selected_model = (
    st.session_state.local_model
    if st.session_state.model_source == "Local"
    else st.session_state.api_model
)

# ✅ Write to file so chatbot_crew.py can read it
write_model_config_to_file(st.session_state.model_source, selected_model)
write_tool_to_file(st.session_state.get("selected_tool", "None"))

# Only initialize the flow once
if "chatbot_flow" not in st.session_state:
    initial_state = ChatBotState(
        conversation_history=st.session_state.conversation_history.copy()
    )
    st.session_state.chatbot_flow = ChatBotFlow(initial_state)




with right_col:
    st.title("🤖 My ChatBot")

    st.markdown("👋 Hello! Ask me anything...")

    # --- Chat History Box ---
    chat_html = '<div class="chat-box">'
    for entry in st.session_state.conversation_history_full:
        if entry["role"] == "user":
            chat_html += f'<div class="chat-entry user">You: {entry["content"]}</div>'
        elif entry["role"] == "assistant":
            chat_html += f'<div class="chat-entry assistant">AI: {entry["content"]}</div>'
    chat_html += '</div>'
    st.markdown(chat_html, unsafe_allow_html=True)

    # --- Input Box Aligned Below Chat ---
    with st.container():
        st.markdown('<div class="bottom-input-container">', unsafe_allow_html=True)

        col1, col2 = st.columns([5, 1])
        with col1:
            st.text_area(
                label = "Message",
                placeholder="Write your prompt here...",
                height=70,
                label_visibility="collapsed",
                key="input"
            )
        with col2:
            st.button("➤", on_click=send_and_clear, key="send_button")

        st.markdown('</div>', unsafe_allow_html=True)













# # --- Model Selection ---
# left_col, right_col = st.columns([1, 3])  # Left for selectors, right for chat

# with left_col:
#     st.markdown("### Settings")

#     model_source = st.selectbox("Model Source", ["Local", "API"], key="model_source")
    
#     if model_source == "Local":
#         model_name = st.selectbox("Local Model", ["gemma3", "llama3.2", "granite3-dense"], key="local_model")
#     else:
#         model_name = st.selectbox("API Model", ["gemini-2.5-flash", "gemini-2.5-pro", "gemini-2.0-flash", "gemini-1.5-flash"], key="api_model")








# # --- Conversation History ---

# st.markdown('<div class="chat-wrapper">', unsafe_allow_html=True)

# st.title("🤖 Personal ChatBot")

# # Scrollable chat box
# # Build chat content as a single HTML block
# chat_html = '<div class="chat-box">'

# for entry in st.session_state.conversation_history_full:
#     if entry["role"] == "user":
#         chat_html += f'\n\n<div class="chat-entry user">You: {entry["content"]}</div>'
#     elif entry["role"] == "assistant":
#         chat_html += f'\n\n<div class="chat-entry assistant">AI: {entry["content"]}</div>'

# chat_html += '</div>'

# # Render the entire chat box
# st.markdown(chat_html, unsafe_allow_html=True)






# # --- Bottom fixed input box like ChatGPT ---
# with st.container():
#     st.markdown('<div class="bottom-input-container">', unsafe_allow_html=True)
    
#     col1, col2 = st.columns([5, 1])
#     with col1:
#         user_input = st.text_area(
#             "Message",
#             height=70,
#             label_visibility="collapsed",
#             key="input",
#         )
#     with col2:
#         send = st.button("➤", on_click=send_and_clear, key="send_button")

#     st.markdown('</div>', unsafe_allow_html=True)







