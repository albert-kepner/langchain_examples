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

concept = "340B rebate pilot"

prompt = prompt_template.format(concept=concept)

print(prompt)

model = init_chat_model("gpt-4o-mini", model_provider="openai")

response = model.invoke(prompt)

print(response.text)


