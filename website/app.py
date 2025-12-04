import os
from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle
import numpy as np
from dotenv import load_dotenv

load_dotenv()

print("🚀 Starting Physical AI Textbook API...")

# Load retriever data (simplified)
documents = []
files = []
vectorizer = None
X = None

try:
    with open("retriever.pkl", "rb") as f:
        data = pickle.load(f)
        print("✅ Pickle file loaded successfully")
        
        # Extract data with safety checks
        vectorizer = data.get("vectorizer", None)
        X = data.get("X", None)
        documents = data.get("documents", [])
        files = data.get("files", [])
        
        print(f"📊 Data loaded: {len(documents)} documents, {len(files)} files")
        if vectorizer:
            print("✅ Vectorizer loaded")
        if X is not None:
            print(f"✅ TF-IDF matrix shape: {X.shape}")
            
except Exception as e:
    print(f"⚠️ Error loading pickle: {e}")
    # Fallback data
    documents = [
        "Physical AI refers to artificial intelligence systems that interact with the physical world through robots or other embodied agents.",
        "Humanoid Robotics focuses on creating robots that resemble the human form and can perform human-like tasks.",
        "ROS 2 (Robot Operating System) is middleware for robot control, providing tools and libraries for building robot applications.",
        "NVIDIA Isaac Sim is a simulation platform for training AI robots in virtual environments.",
        "Gazebo is a physics simulator used for testing robots in digital environments before physical deployment."
    ]
    files = ["chapter1.txt", "chapter2.txt", "chapter3.txt", "chapter4.txt", "chapter5.txt"]
    print("✅ Using fallback data")

app = FastAPI()

# CORS setup
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

def get_smart_response(question, top_docs):
    """Generate intelligent response without external API"""
    
    question_lower = question.lower()
    
    # Keyword-based intelligent responses
    responses = {
        "what is physical ai": "Physical AI refers to artificial intelligence systems that interact with the physical world through robots or other embodied agents. Unlike purely digital AI, Physical AI can manipulate real objects and navigate physical environments.",
        
        "what is ros": "ROS 2 (Robot Operating System) is middleware for robot software development. It provides communication infrastructure (nodes, topics, services) that allows different robot components to work together seamlessly.",
        
        "what is gazebo": "Gazebo is a 3D robotics simulator that provides physics simulation and sensor modeling. It allows developers to test robots in virtual environments before building physical prototypes.",
        
        "what is humanoid robotics": "Humanoid Robotics focuses on creating robots that resemble the human form. These robots can perform human-like tasks and operate in environments designed for humans.",
        
        "what is nvidia isaac": "NVIDIA Isaac is a platform for AI-powered robotics, including Isaac Sim for photorealistic simulation and Isaac ROS for accelerated perception and manipulation tasks.",
        
        "how do robots work": "Robots work by combining sensors (to perceive), processors (to think/plan), and actuators (to act). They use software like ROS 2 to coordinate these components.",
        
        "what is robot simulation": "Robot simulation involves creating digital twins of robots in virtual environments using tools like Gazebo or NVIDIA Isaac Sim. This allows testing without physical hardware."
    }
    
    # Check for exact matches
    for key in responses:
        if key in question_lower:
            return responses[key]
    
    # Check for keyword matches
    if "physical" in question_lower and "ai" in question_lower:
        return responses["what is physical ai"]
    elif "ros" in question_lower:
        return responses["what is ros"]
    elif "gazebo" in question_lower:
        return responses["what is gazebo"]
    elif "humanoid" in question_lower:
        return responses["what is humanoid robotics"]
    elif "isaac" in question_lower:
        return responses["what is nvidia isaac"]
    elif "simulation" in question_lower:
        return responses["what is robot simulation"]
    
    # If no keyword match, use document context
    if top_docs:
        return f"Based on the textbook: {top_docs[0][:300]}..."
    
    # Default response
    return "I can answer questions about Physical AI, ROS 2, Gazebo, Humanoid Robotics, and NVIDIA Isaac. Please ask about these topics."

@app.get("/")
def home():
    return {
        "message": "Physical AI Textbook RAG API",
        "status": "running",
        "documents": len(documents),
        "version": "1.0",
        "endpoints": ["/health", "/ask?q=question", "/debug"]
    }

@app.get("/health")
def health():
    return {"status": "healthy", "timestamp": "now"}

@app.get("/debug")
def debug():
    return {
        "documents_count": len(documents),
        "sample_document": documents[0][:100] + "..." if documents else "No documents",
        "files_count": len(files),
        "vectorizer": "loaded" if vectorizer else "not loaded",
        "X_matrix": "loaded" if X is not None else "not loaded"
    }

@app.get("/ask", response_model=AskResponse)
def ask(q: str = Query(..., min_length=2)):
    """Main endpoint to ask questions"""
    try:
        print(f"\n🔍 Question received: '{q}'")
        
        # Simple keyword matching (no TF-IDF if not available)
        if vectorizer is not None and X is not None:
            try:
                query_vec = vectorizer.transform([q])
                scores = (X @ query_vec.T).toarray().ravel()
                top_indices = scores.argsort()[::-1][:3]
                
                top_docs = []
                top_files = []
                for idx in top_indices:
                    if idx < len(documents):
                        top_docs.append(documents[idx])
                    if idx < len(files):
                        top_files.append(files[idx])
                
                print(f"✅ Found {len(top_docs)} relevant documents")
                
            except Exception as e:
                print(f"⚠️ TF-IDF error, using simple match: {e}")
                top_docs = documents[:2]
                top_files = files[:2]
        else:
            # Use first few documents as fallback
            top_docs = documents[:2]
            top_files = files[:2]
            print("ℹ️ Using simple document selection")
        
        # Generate answer
        answer = get_smart_response(q, top_docs)
        
        # Ensure sources list
        if not top_files:
            top_files = ["Physical AI Textbook"]
        
        print(f"📤 Sending answer ({len(answer)} chars)")
        
        return AskResponse(
            answer=answer,
            sources=top_files
        )
        
    except Exception as e:
        print(f"❌ Error in /ask: {str(e)}")
        # Still return a valid response
        return AskResponse(
            answer="I can help you learn about Physical AI and Robotics. Please try asking about: ROS 2, Gazebo simulation, Humanoid robots, or NVIDIA Isaac.",
            sources=["Physical AI Textbook"]
        )

if __name__ == "__main__":
    import uvicorn
    print("\n" + "="*50)
    print("🤖 PHYSICAL AI TEXTBOOK API")
    print("="*50)
    print(f"📚 Documents: {len(documents)}")
    print(f"📁 Files: {len(files)}")
    print("🌐 Server: http://localhost:8000")
    print("🔗 Test: http://localhost:8000/ask?q=What is Physical AI?")
    print("🔗 Health: http://localhost:8000/health")
    print("="*50)
    uvicorn.run(app, host="0.0.0.0", port=8000)