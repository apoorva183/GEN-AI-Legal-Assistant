# import os
# from groq import Groq

# # ✅ Set API Key Directly (Replace with your actual API key)
# GROQ_API_KEY = "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"

# # ✅ Initialize Groq Client
# if not GROQ_API_KEY:
#     raise ValueError("❌ Error: GROQ_API_KEY is missing! Please add your API key.")

# client = Groq(api_key=GROQ_API_KEY)

# def speculative_rag_response(user_query):
#     """Generates a speculative legal answer before document retrieval using Groq API."""
#     speculative_prompt = (
#         "You are an expert AI legal assistant. Based on general legal principles, "
#         "provide a speculative answer to the following question before retrieving legal documents.\n\n"
#         f"User Query: {user_query}\n"
#         "Speculative Answer:"
#     )
    
#     response = client.chat.completions.create(
#         model="mixtral-8x7b-32768",
#         messages=[{"role": "system", "content": speculative_prompt}]
#     )
    
#     return response.choices[0].message.content.strip()


import os
from groq import Groq

# Set API Key
GROQ_API_KEY = ""
if not GROQ_API_KEY:
    raise ValueError("❌ Error: GROQ_API_KEY is missing! Please add your API key.")

client = Groq(api_key=GROQ_API_KEY)

def call_groq_api(prompt):
    """Handles Groq API call and error handling."""
    try:
        response = client.chat.completions.create(
            model="mixtral-8x7b-32768",
            messages=[
                {"role": "system", "content": "You are an expert AI legal assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content.strip() if response.choices else "⚠️ Error: No valid response received."
    except Exception as e:
        return f"⚠️ API Error: {str(e)}"

def speculative_rag_response(user_query):
    """Generates a speculative legal answer before document retrieval using Groq API."""
    speculative_prompt = (
        "Based on general legal principles, provide a speculative answer "
        "to the following question before retrieving legal documents.\n\n"
        f"User Query: {user_query}\n"
        "Speculative Answer:"
    )

    speculative_answer = call_groq_api(speculative_prompt)

    # Step 2: Retrieve legal documents (Simulated function)
    retrieved_docs = retrieve_legal_documents(user_query)

    # Step 3: Compare speculative answer with retrieved documents
    final_answer_prompt = (
        "Compare the following speculative legal answer with retrieved legal documents "
        "and refine the final response for better accuracy.\n\n"
        f"Speculative Answer: {speculative_answer}\n\n"
        f"Retrieved Documents: {retrieved_docs}\n\n"
        "Final Answer:"
    )

    final_answer = call_groq_api(final_answer_prompt)
    return final_answer

def retrieve_legal_documents(query):
    """Simulated function to retrieve legal documents related to the query."""
    # In real implementation, this would connect to a database or vector search system.
    return "Legal case laws, statutes, and relevant documents related to the query."

# Example usage
if __name__ == "__main__":
    user_query = "What are the legal implications of breaking a non-compete agreement?"
    result = speculative_rag_response(user_query)
    print("Final Legal Answer:\n", result)
