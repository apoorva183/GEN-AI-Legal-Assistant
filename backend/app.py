from fastapi import FastAPI, HTTPException, File, UploadFile
import shutil
import os
from query_refinement import refine_query, generate_hyde_document
from speculative_rag import speculative_rag_response
from human_review import human_review_needed
from document_loader import load_contracts, process_user_uploaded_pdf

app = FastAPI()
vector_store = None  # Global FAISS vector store
UPLOAD_DIR = "data/user_uploads/"


@app.on_event("startup")
def startup_event():
    global vector_store
    try:
        vector_store = load_contracts()
        if not vector_store:
            print("⚠️ Warning: No contracts loaded. Retrieval might not work.")
    except Exception as e:
        print(f"❌ Error loading contracts: {e}")
        vector_store = None  # Prevent backend crash

@app.post("/upload/")
async def upload_pdf(file: UploadFile = File(...)):
    """Allows users to upload a legal PDF and processes it for retrieval."""
    if not os.path.exists(UPLOAD_DIR):
        os.makedirs(UPLOAD_DIR)

    file_path = os.path.join(UPLOAD_DIR, file.filename)
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        user_vector_store = process_user_uploaded_pdf(file_path)
        return {"message": "✅ File uploaded and processed successfully!", "file": file.filename}
    except Exception as e:
        return {"error": f"❌ Failed to process uploaded PDF: {e}"}


def summarize_legal_content(raw_text):
    """Uses AI to summarize and extract key clauses from retrieved contract text."""
    summary_prompt = (
        "You are an AI legal assistant. Summarize the key clauses and obligations from the following legal contract text "
        "while keeping it concise and legally accurate:\n\n"
        f"{raw_text}\n\n"
        "Summary of key legal clauses:"
    )

    response = speculative_rag_response(summary_prompt)  
    return response.strip()


@app.get("/query")
def process_query(user_query: str, use_uploaded: bool = False):
    """Processes user query using Advanced RAG techniques with HyDE, Speculative RAG, and FAISS retrieval."""
    global vector_store

    
    if use_uploaded:
        uploaded_files = os.listdir(UPLOAD_DIR)
        if not uploaded_files:
            raise HTTPException(status_code=400, detail="❌ No uploaded document found.")
        
        latest_file = sorted(uploaded_files, key=lambda x: os.path.getmtime(os.path.join(UPLOAD_DIR, x)))[-1]
        uploaded_vector_store = process_user_uploaded_pdf(os.path.join(UPLOAD_DIR, latest_file))

        if uploaded_vector_store is None:
            raise HTTPException(status_code=500, detail="❌ Failed to process uploaded contract.")

        vector_store = uploaded_vector_store  # ✅ Use uploaded document for retrieval

    else:
        # If no uploaded document is selected, reset to default contracts
        vector_store = load_contracts()
    
    if vector_store is None:
        raise HTTPException(status_code=500, detail="❌ Vector store is not initialized. Check if legal contracts were loaded.")

    try:
        # Step 1: HyDE - Generate Hypothetical Document Embeddings
        hyde_generated_text = generate_hyde_document(user_query)

        # Step 2: Query Refinement
        refined_query = refine_query(user_query)

        # Step 3: Retrieve Legal Context from FAISS
        legal_contexts = vector_store.similarity_search(hyde_generated_text, k=3)
        retrieved_text = "\n\n".join([doc.page_content for doc in legal_contexts])

        # Step 4: Human-in-the-loop Check for Irrelevant Contract Retrieval
        if not retrieved_text.strip():
            return {"response": "⚠️ No relevant contract information found. This requires human legal intervention."}

        # Step 5: AI Speculative Response
        speculative_response = speculative_rag_response(refined_query)

        # Step 6: AI-Generated Structured Response
        structured_summary = summarize_legal_content(retrieved_text)
        final_response = f"🔍 **Based on legal contracts:**\n{structured_summary}"

        # Step 7: Human-in-the-loop - Flag Uncertainty
        if human_review_needed(final_response, user_query):
            return {"response": "⚠️ This response is uncertain and requires human legal review. Please consult a lawyer."}

        return {"response": final_response}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"❌ Query processing failed: {str(e)}")
