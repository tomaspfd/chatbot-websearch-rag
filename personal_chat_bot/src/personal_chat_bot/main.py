#!/usr/bin/env python
from random import randint

from pydantic import BaseModel

from crewai.flow import Flow, listen, start

from .crews.chatbot_crew.chatbot_crew import ChatBotCrew
from .crews.summarizer_crew.summarizer_crew import SummarizerCrew


class ChatBotState(BaseModel):
    conversation_history : list[dict] = []


    


class ChatBotFlow(Flow[ChatBotState]):

    @start()
    #@listen()
    def llm_response(self):

        if not self.state.conversation_history:
            return  "No input was provided."

        # Pass the entire conversation history to the model

        result = (
            ChatBotCrew()
            .crew()
            .kickoff(inputs={"conversation_history": self.state.conversation_history})
        )

        # Append the model's response to the conversation history
        self.state.conversation_history.append({"role": "assistant", "content": str(result)})


    @listen(llm_response)
    def summarize_if_needed(self):
        # Find last summary (system message)
        last_system_index = max(
            (i for i, msg in enumerate(self.state.conversation_history) if msg["role"] == "system"),
            default=-1
        )

        # Count how many messages since then
        messages_since = len(self.state.conversation_history) - (last_system_index + 1)

        if messages_since < 8:
            return

        # 🔪 Split: Summarize the older half 
        old_messages = self.state.conversation_history[:-4]
        recent_messages = self.state.conversation_history[-4:]

        # 🧾 Convert old messages to plain text
        conversation_text = "\n".join(
            f"{msg['role'].capitalize()}: {msg['content']}"
            for msg in old_messages
        )

        # 🧠 Kick off summarizer crew

        summary = SummarizerCrew().crew().kickoff(inputs={
            "conversation_to_summarize": conversation_text
        }) 

        # 🪄 Replace old history with a single summary
        self.state.conversation_history = (
            [{"role": "system", "content": f"Conversation Summary: {summary}"}]
            + recent_messages
        )

        


        






def plot():
    ChatBot_flow = ChatBotFlow()
    ChatBot_flow.plot()


if __name__ == "__main__":
    conversation_history = []
    chatbot_flow = ChatBotFlow()
    user_input = input("Enter: ")
    while user_input != "exit":
        conversation_history.append({"role": "user", "content": user_input})
        chatbot_flow.state.conversation_history = conversation_history.copy()
        chatbot_flow.kickoff()
        conversation_history = chatbot_flow.state.conversation_history.copy()
        print(f"AI: {conversation_history[-1]['content']}")
        user_input = input("Enter: ")


