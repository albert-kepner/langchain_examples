from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate

from pydantic import BaseModel, Field, ValidationError
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
        description="The text of an FDA drug recall product description",
        pattern=r"\WNDC\W", min_length=20, max_length=2000,
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
example01 = """
Isotretinoin Capsules, USP, 30 mg, Rx Only, 10 count Prescription Pack, Manufactured for: Teva Pharmaceuticals USA, Inc.,
Parsippany, NJ 07054, NDC 0591-2435-15 (carton), NDC 0591-2435-45 (blister pack).
"""

example02 = """
Isotretinoin Capsules, USP, 40 mg, 10 count Prescription Pacs, Rx only, Manufactured for: 
Teva Pharmaceuticals USA, Inc., Parsippany, NJ 07054, NDC 0591-2436-15 (carton), NDC 0591-2436-45 (blister pack).
"""

example03 = """
Dexamethasone Sodium Phosphate Injection, USP, 100 mg/ 10 mL, (10 mg/mL), 10x10 mL Multiple Dose Vials, 
Rx only, Manufactured for: Somerset Therapeutics, LLC., Somerset, NJ 08873, NDC carton: 70069-025-10; NDC vial: 70069-025-01
"""

prompt_template = PromptTemplate.from_template(prompt_template_str)


def get_response(input):
    try:
        # Directly validates the JSON string
        recall = RecallNotice(text=input)
        print(f"Recall parsed OK.")
    except ValidationError as e:
        print(e.json())
        return f"Invalid Input: {input}"
    prompt = prompt_template.format(input=input)
    response = structured_llm.invoke(prompt)
    print(f"Recall found for product: {response.product_name}")
    return response


print(get_response(example01))

print(get_response(example02))

print(get_response(example03))

