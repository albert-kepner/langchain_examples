# Your code goes here
from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

import os 
from dotenv import load_dotenv

load_dotenv()

# OPEN_API_KEY =

prompt_template_str = """
Your task is to explain the concept of **{concept}** to me in a way that is:

1. Clear and intuitive
2. Concise (in under 100 words)
3. Tailored specifically to me and what I already know

Use the following information about me to personalize your explanations:

- Role: Business Analyst and Data Engineer
- Industry: Healthcare
- Goal: Building LLM-powered apps for healthcare analytics and self-service business intelligence

The personalization should be subtle and natural. Avoid forced references to my background that don't genuinely enhance understanding.
"""

prompt_template = PromptTemplate.from_template(prompt_template_str)

model = init_chat_model("gpt-4o-mini", model_provider="openai")

def generate_explanation(concept):
  prompt = prompt_template.format(concept=concept)
  response = model.invoke(prompt)
  return response.text
  
import gradio as gr

demo = gr.Interface(
    fn=generate_explanation,
    inputs=[gr.Textbox(label="Concept", lines=1)],
    outputs=[gr.Textbox(label="Explanation", lines=5)],
    flagging_mode="never",
    title="Concept Explainer",
    description="Enter any term to get a personalized explanation"
)

# demo.launch()