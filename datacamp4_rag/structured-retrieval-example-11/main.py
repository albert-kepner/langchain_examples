# -----NEW CODE-----#


def format_results_for_llm(results_df: pd.DataFrame) -> str:
    """Format query results for LLM consumption."""
    if results_df.empty:
        return "No results found"

    # Convert DataFrame to readable format
    return results_df.to_string(index=False)


generate_response_prompt_template_str = """
Given the results of a hotel search and the original user query, create a user-friendly response following these guidelines:

1. Start with a brief welcome acknowledging the search parameters
2. Present each hotel with:
   - A paragraph containing name and location and 2-3 sentences highlighting the hotel's unique features
       - Use selective bold text for emphasis
       - Keep descriptions concise but informative, focusing on the most relevant features for the user's request.
   - Followed by price and availability as bullet points
3. End with a simple offer to provide more information

Original User Query: {user_query}

Hotel Search Results:
{hotels_data}

Please create a friendly, informative response:"""

# Create the response generation prompt
generate_response_prompt = PromptTemplate(
    template=generate_response_prompt_template_str,
    input_variables=["hotels_data"],
    partial_variables={"user_query": user_query},
)

# Response Generation Chain (handles DataFrame → String → Response)
generate_response = format_results_for_llm | generate_response_prompt | model

# Complete RAG Pipeline
structured_rag = retrieve_knowledge | generate_response

result = structured_rag.invoke({"user_query": user_query})

print("============= RESULT =============")
print(result.text)

