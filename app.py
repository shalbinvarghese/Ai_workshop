import os
import gradio
from groq import Groq


client = Groq(
    api_key=os.environ.get("GROQ_API_KEY")
)
def initialize_messages():
    return [{"role": "system",
             "content": """You are an experienced healthcare consultant with deep knowledge of medical practices, patient care, and health regulations in India. Your role is to assist people by providing clear, evidence-based guidance on health-related topics, explaining medical conditions, preventive care, treatment options, and healthcare procedures in a professional and responsible manner. You offer information for educational purposes while encouraging users to seek proper diagnosis and treatment from qualified medical professionals whenever necessary."""}]
messages_prmt = initialize_messages()
def customLLMBot(user_input, history):
    global messages_prmt

    messages_prmt.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        messages=messages_prmt,
        model="llama-3.3-70b-versatile",
    )
    print(response)
    LLM_reply = response.choices[0].message.content
    messages_prmt.append({"role": "assistant", "content": LLM_reply})

    return LLM_reply
iface = gradio.ChatInterface(customLLMBot,
                     chatbot=gradio.Chatbot(height=300),
                     textbox=gradio.Textbox(placeholder="Ask me a question related to health"),
                     title="Health ChatBot",
                     description="Chat bot for health",
                     theme="soft",
                     examples=[
                         ["Hello I'm your AI health assistant.How can I help you today"] ,
                             ["What are common cold symptoms"]
                     ])
iface.launch(share=True)
