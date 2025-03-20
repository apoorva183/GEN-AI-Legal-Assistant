import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.title("⚖️ AI-Powered Legal Assistant")
st.write("Ask legal questions and get contract-based answers.")

# Upload PDF Section
st.subheader("📄 Upload a Legal Document")
uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")

if uploaded_file:
    files = {"file": uploaded_file.getvalue()}
    response = requests.post(f"{API_URL}/upload/", files=files)
    if response.status_code == 200:
        st.success("✅ File uploaded successfully!")

# Query Input Section
st.subheader("💬 Ask a Legal Question")
user_query = st.text_input("Enter your legal question:")

use_uploaded = st.checkbox("Use my uploaded contract instead of sample contracts")

if st.button("Get Answer"):
    if user_query.strip():
        response = requests.get(f"{API_URL}/query", params={"user_query": user_query, "use_uploaded": use_uploaded})
        if response.status_code == 200:
            st.write("### 🤖 AI Response:")
            st.success(response.json()["response"])
        else:
            st.error("Error fetching response. Please check the backend.")
    else:
        st.warning("Please enter a valid query.")
