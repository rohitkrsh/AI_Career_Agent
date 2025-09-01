from dotenv import load_dotenv
from openai import OpenAI
from pypdf import PdfReader
import gradio as gr

load_dotenv(override=True)
openai = OpenAI()

# Define the person's name first
name = "Rohit Singh"

reader = PdfReader("linkedin_profile.pdf")

linkedin = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        linkedin += text

print(linkedin)

with open("summary.txt", "r") as f:
    summary = f.read()

system_prompt = f"You are acting as {name}. You are answering questions on {name}'s website, \
particularly questions related to {name}'s career, background, skills and experience. \
Your responsibility is to represent {name} for interactions on the website as faithfully as possible. \
You are given a summary of {name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer, say so."

system_prompt += f"\n\n## Summary:\n{summary}\n\n## LinkedIn Profile:\n{linkedin}\n\n"
system_prompt += f"With this context, please chat with the user, always staying in character as {name}."

def chat(message, history):
    # Convert Gradio history format to OpenAI format
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add conversation history
    for human, assistant in history:
        messages.append({"role": "user", "content": human})
        messages.append({"role": "assistant", "content": assistant})
    
    # Add current user message
    messages.append({"role": "user", "content": message})
    
    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini", 
            messages=messages,
            max_tokens=500
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Sorry, I encountered an error: {str(e)}"

# Create and launch the Gradio interface
demo = gr.ChatInterface(
    fn=chat,
    title=f"Chat with {name}",
    description=f"Ask me anything about my career, background, skills, and experience!",
    examples=[
        "Tell me about your background",
        "What are your key skills?",
        "What's your experience in software engineering?",
        "Where do you currently work?"
    ]
)

if __name__ == "__main__":
    demo.launch(share=False)