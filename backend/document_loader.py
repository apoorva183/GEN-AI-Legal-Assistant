import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

# ✅ Use absolute path to ensure correct file location
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data/contracts/")

def load_contracts():
    """Load and process legal contracts from PDFs into FAISS."""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)  # ✅ Ensures `data/contracts/` exists

    files = [f for f in os.listdir(DATA_DIR) if f.endswith(".pdf")]
    if not files:
        print(f"⚠️ Warning: No PDFs found in '{DATA_DIR}'. Retrieval might not work!")
        return None  

    all_text = ""
    for pdf_file in files:
        file_path = os.path.join(DATA_DIR, pdf_file)  # ✅ Use absolute path
        print(f"📄 Processing file: {file_path}")  # Debugging print

        loader = PyPDFLoader(file_path)
        docs = loader.load()
        all_text += "\n\n".join([doc.page_content for doc in docs])

    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([all_text])

    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embeddings)

def process_user_uploaded_pdf(file_path):
    """Processes a user-uploaded PDF and creates a FAISS vector store for retrieval."""
    from langchain_community.document_loaders import PyPDFLoader

    print(f"📄 Processing uploaded file: {file_path}")

    loader = PyPDFLoader(file_path)
    docs = loader.load()

    # Extract actual text content
    text_content = "\n\n".join([doc.page_content for doc in docs])
    if not text_content.strip():
        raise ValueError("❌ No valid text found in uploaded PDF!")

    # Chunk the extracted text properly
    splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = splitter.create_documents([text_content])

    if not chunks:
        raise ValueError("❌ No valid chunks generated from uploaded PDF!")

    # Create a FAISS index for the uploaded document
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    return FAISS.from_documents(chunks, embeddings)


