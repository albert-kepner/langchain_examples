from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

# Model: gpt-4o-mini | Provider: openai

prompt_template_str = """
Please explain the clinical term {concept} in simple language for business users. The response
should be no more than 100 words.
"""

prompt_template = PromptTemplate.from_template(prompt_template_str)

model = init_chat_model("gpt-4o-mini", model_provider="openai")

def generate_explanation(concept):
  prompt = prompt_template.format(concept=concept)
  response = model.invoke(prompt)
  return response.text

concept = "systolic pressure"

explanation = generate_explanation(concept)

print(explanation)
  
import gradio as gr

demo = gr.Interface(
    fn=generate_explanation,
    inputs=[gr.Textbox(label="Concept", lines=1)],
    outputs=[gr.Textbox(label="Explanation", lines=5)],
    flagging_mode="never",
    title="Concept Explainer",
    description="Enter any term to get a personalized explanation"
)