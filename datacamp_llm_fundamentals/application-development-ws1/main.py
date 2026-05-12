from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field
from typing import Optional

# from dotenv import load_dotenv
# load_dotenv()

class RecallProductInfo(BaseModel):
    ndc_numbers: list[str] = Field(description="The NDC numbers")
    product_name: str = Field(description="The name of the product being recalled")
    dosage_form: Optional[str] = Field(description="The dosage form of the product")
    strength: Optional[str] = Field(description="The size of strength of a single product dose")

class RecallNotice(BaseModel):
    text: str = Field(
        description="The text of an FDA drug recall product description"
    )
    

model = init_chat_model("gpt-4o-mini", model_provider="openai")

# Create a structured LLM that returns validated Pydantic objects
structured_llm = model.with_structured_output(RecallProductInfo)

prompt_template_str = """
You should extract structured text from an FDA drug recall product description.
The field ndc_nubmers should contain a list of the NDC codes found.
The field product_name probably occurs first in the description.
Also extract optional fields dosage_form and strengh, if available.

Product Description: {input}
"""

prompt_template = PromptTemplate.from_template(prompt_template_str)


def get_response(input):
    prompt = prompt_template.format(input=input)
    response = structured_llm.invoke(prompt)
    return response


# print(get_response("..."))

