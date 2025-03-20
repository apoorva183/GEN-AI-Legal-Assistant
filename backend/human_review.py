# def human_review_needed(answer, query):
#     """Determines if the AI-generated response is uncertain and requires human intervention."""
    
#     low_confidence_phrases = [
#         "I'm not sure", "unclear", "it depends", "consult a lawyer", "varies by jurisdiction",
#         "depends on the contract", "seek legal advice", "not specified in this document"
#     ]
    
#     # ✅ Check if the response is vague or uncertain
#     if any(phrase in answer.lower() for phrase in low_confidence_phrases):
#         return True  

#     # ✅ If the question is **not contract-related**, flag for human review
#     contract_keywords = ["lease", "agreement", "contract", "terms", "termination", "dispute", "obligations"]
#     if not any(keyword in query.lower() for keyword in contract_keywords):
#         return True  

#     return False


import re

def human_review_needed(answer, query):
    """Determines if the AI-generated response is uncertain and requires human intervention."""

    # Common vague/uncertain phrases
    low_confidence_phrases = [
        "I'm not sure", "unclear", "it depends", "consult a lawyer", "varies by jurisdiction",
        "depends on the contract", "seek legal advice", "not specified in this document",
        "I am not a lawyer", "I cannot guarantee accuracy", "legal professionals should be consulted"
    ]
    
    # AI-generated disclaimers
    ai_disclaimers = [
        "I am an AI", "this is not legal advice", "I cannot provide definitive answers", 
        "I am not authorized", "for informational purposes only"
    ]

    # Check if the response is vague or uncertain
    if any(re.search(rf"\b{re.escape(phrase)}\b", answer, re.IGNORECASE) for phrase in low_confidence_phrases + ai_disclaimers):
        return True  

    # Flag if query is **not legal in nature** (not just contracts)
    legal_keywords = [
        "lease", "agreement", "contract", "terms", "termination", "dispute", "obligations",
        "liability", "court", "statute", "regulation", "damages", "lawsuit", "plaintiff", "defendant",
        "intellectual property", "patent", "copyright", "trademark", "breach", "fiduciary", "warranty"
    ]
    
    if not any(re.search(rf"\b{keyword}\b", query, re.IGNORECASE) for keyword in legal_keywords):
        return True  

    return False
