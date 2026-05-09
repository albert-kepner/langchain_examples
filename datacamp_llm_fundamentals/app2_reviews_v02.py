from langchain.chat_models import init_chat_model
from pydantic import BaseModel, Field
from typing import Optional
from devtools import pprint


# Define the Pydantic model


class Opinion(BaseModel):
    topic: str = Field(description="The topic of the opinion")
    sentiment: str = Field(description="The sentiment of the opinion")
    problem: Optional[str] = Field(description="The problem of the opinion, if any.")
    suggested_solution: Optional[str] = Field(
        description="The suggested solution of the opinion, if any."
    )


class StructuredReview(BaseModel):
    review_id: str = Field(description="The ID of the review", pattern=r"^R\d{5}$")
    overall_sentiment: str = Field(description="The sentiment of the review")
    notable_phrases: list[str] = Field(description="The notable phrases of the review")
    opinions: list[Opinion] = Field(description="The opinions of the review")


llm = init_chat_model(model="gpt-4.1-mini", temperature=0)

# Create a structured LLM that returns validated Pydantic objects
structured_llm = llm.with_structured_output(StructuredReview)


# This is the schema that gets sent to the LLM
pprint(StructuredReview.model_json_schema())