# import os
# from groq import Groq

# # ✅ Set API Key Directly (Replace with your actual API key)
# GROQ_API_KEY = "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"

# # ✅ Initialize Groq Client
# if not GROQ_API_KEY:
#     raise ValueError("❌ Error: GROQ_API_KEY is missing! Please add your API key.")

# client = Groq(api_key=GROQ_API_KEY)

# def generate_hyde_document(user_query):
#     """Generates a hypothetical document (HyDE) for better retrieval."""
#     prompt = (
#         "You are an AI legal assistant. Generate a hypothetical legal document that could answer the following query.\n\n"
#         f"User Query: {user_query}\n"
#         "Hypothetical Answer (HyDE):"
#     )

#     response = client.chat.completions.create(
#         model="mixtral-8x7b-32768",
#         messages=[{"role": "system", "content": prompt}]
#     )
    
#     return response.choices[0].message.content.strip()

# def refine_query(user_query):
#     """Rewrites vague legal queries into structured questions using Groq API."""
#     prompt = (
#         "You are a legal AI specializing in contract law. Rewrite the following vague legal query "
#         "into a precise and structured legal question for better retrieval:\n\n"
#         f"User Query: {user_query}\n"
#         "Refined Query:"
#     )

#     response = client.chat.completions.create(
#         model="mixtral-8x7b-32768",
#         messages=[{"role": "system", "content": prompt}]
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
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "You are an AI legal assistant."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content.strip() if response.choices else "⚠️ Error: No valid response received."

def generate_hyde_document(user_query):
    """Generates a hypothetical legal document for retrieval (HyDE technique)."""
    prompt = (
        "Generate a hypothetical legal document that could answer the following query.\n\n"
        f"User Query: {user_query}\n"
        "Hypothetical Answer (HyDE):"
    )
    return call_groq_api(prompt)

def refine_query(user_query):
    """Refines a vague legal question into a precise legal query."""
    prompt = (
        "Rewrite the following vague legal query into a precise and structured legal question:\n\n"
        f"User Query: {user_query}\n"
        "Refined Query:"
    )
    return call_groq_api(prompt)

