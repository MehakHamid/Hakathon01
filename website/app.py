import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from dotenv import load_dotenv
import google.generativeai as genai
from numpy.linalg import norm

load_dotenv()

# Gemini Configuration
API_KEY = os.getenv("GEMINI_API_KEY")
MODEL = os.getenv("GEMINI_MODEL", "models/gemini-2.0-flash")

print(f"🔧 Using Gemini Model: {MODEL}")

if API_KEY:
    try:
        genai.configure(api_key=API_KEY)
        print("✅ Gemini AI configured successfully")
        GEMINI_ENABLED = True
    except Exception as e:
        print(f"❌ Gemini configuration failed: {e}")
        GEMINI_ENABLED = False
else:
    print("⚠️ GEMINI_API_KEY not found in .env file")
    print("ℹ️ Using mock responses for testing")
    GEMINI_ENABLED = False

# Load retriever
try:
    with open("retriever.pkl", "rb") as f:
        data = pickle.load(f)
    
    vectorizer = data["vectorizer"]
    X = data["X"]
    documents = data["documents"]
    files = data["files"]
    print(f"✅ Loaded {len(documents)} documents from retriever.pkl")
except Exception as e:
    print(f"❌ Error loading retriever.pkl: {e}")
    # Fallback data
    documents = [
        "Physical AI refers to artificial intelligence systems that interact with the physical world through robots or other embodied agents.",
        "Humanoid Robotics focuses on creating robots that resemble the human form and can perform human-like tasks.",
        "ROS 2 (Robot Operating System) is middleware for robot control, providing tools and libraries for building robot applications.",
        "NVIDIA Isaac Sim is a simulation platform for training AI robots in virtual environments."
    ]
    files = ["textbook_chapter1.txt", "textbook_chapter2.txt", "textbook_chapter3.txt", "textbook_chapter4.txt"]
    vectorizer = None
    X = None

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AskResponse(BaseModel):
    answer: str
    sources: list

@app.get("/")
def home():
    return {
        "message": "Physical AI Textbook RAG API",
        "status": "running",
        "documents_loaded": len(documents),
        "gemini_enabled": GEMINI_ENABLED,
        "model": MODEL
    }

@app.get("/health")
def health():
    return {"status": "healthy"}

def get_top_documents(query, top_k=3):
    """Get top relevant documents using TF-IDF similarity"""
    if vectorizer is None or X is None:
        return [], []
    
    try:
        query_vec = vectorizer.transform([query])
        scores = (X @ query_vec.T).toarray().ravel()
        
        # Get top indices
        top_indices = scores.argsort()[::-1][:top_k]
        
        # Get documents and files
        top_docs = []
        top_files = []
        
        for idx in top_indices:
            if idx < len(documents):
                top_docs.append(documents[idx])
            if idx < len(files):
                top_files.append(files[idx])
        
        return top_docs, top_files
    except Exception as e:
        print(f"Error in similarity search: {e}")
        return [], []

@app.get("/ask", response_model=AskResponse)
def ask(q: str = Query(..., description="Your question about Physical AI textbook")):
    try:
        print(f"📝 Question received: {q}")
        
        # Get relevant documents
        top_docs, top_files = get_top_documents(q, top_k=3)
        
        if not top_docs:
            return AskResponse(
                answer="I couldn't find relevant information in the textbook for your question.",
                sources=["No sources found"]
            )
        
        # Prepare context
        context = "\n\n---\n\n".join(top_docs)
        
        # Prepare prompt
        prompt = f"""You are an AI teaching assistant for a Physical AI and Humanoid Robotics textbook.

CONTEXT FROM TEXTBOOK:
{context}

QUESTION: {q}

INSTRUCTIONS:
1. Answer based ONLY on the context provided above.
2. If the answer cannot be found in the context, say "I don't know".
3. Keep the answer clear, concise, and educational.
4. Use examples from the context when possible.

ANSWER:"""
        
        # Generate response
        if GEMINI_ENABLED:
            try:
                model = genai.GenerativeModel(MODEL)
                response = model.generate_content(prompt)
                answer = response.text
                print("✅ Gemini response generated")
            except Exception as e:
                print(f"❌ Gemini error: {e}")
                answer = f"Error generating response from Gemini: {str(e)}"
        else:
            # Mock response
            answer = f"""Based on the textbook content:

{top_docs[0][:200]}...

[Note: This is a mock response. Enable Gemini API for full AI answers.]"""
        
        return AskResponse(
            answer=answer,
            sources=top_files
        )
        
    except Exception as e:
        print(f"❌ Error in /ask endpoint: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# Test endpoint
@app.get("/test")
def test_endpoint():
    """Test endpoint to check if everything is working"""
    test_question = "What is Physical AI?"
    top_docs, top_files = get_top_documents(test_question, top_k=2)
    
    return {
        "test_question": test_question,
        "top_documents_found": len(top_docs),
        "gemini_status": "enabled" if GEMINI_ENABLED else "disabled",
        "sample_document": top_docs[0][:100] + "..." if top_docs else "No documents found"
    }

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🚀 Physical AI Textbook RAG API")
    print("="*50)
    print(f"📚 Documents loaded: {len(documents)}")
    print(f"🤖 Gemini enabled: {GEMINI_ENABLED}")
    print(f"🔗 API URL: http://localhost:8000")
    print(f"📖 Ask questions: http://localhost:8000/ask?q=What is Physical AI?")
    print("="*50 + "\n")
    uvicorn.run(app, host="0.0.0.0", port=8000)