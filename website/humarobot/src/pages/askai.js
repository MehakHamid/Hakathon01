import React from 'react';
import Layout from '@theme/Layout';
import ChatBot from '@site/src/components/ChatBot';
import './AskAIPage.css'; // We'll create this

function AskAIPage() {
  return (
    <Layout 
      title="Ask AI Assistant | Physical AI Textbook" 
      description="Intelligent AI assistant for Physical AI & Humanoid Robotics textbook. Get instant answers using RAG technology."
    >
      <div className="askai-container">
        {/* Hero Section */}
        <div className="askai-hero">
          <div className="hero-content">
            <div className="robot-icon">🤖</div>
            <h1 className="hero-title">AI Textbook Assistant</h1>
            <p className="hero-subtitle">
              Your intelligent companion for learning Physical AI & Humanoid Robotics
            </p>
            <div className="hero-badges">
              <span className="badge">RAG Powered</span>
              <span className="badge">Context-Aware</span>
              <span className="badge">Instant Answers</span>
            </div>
          </div>
        </div>

        {/* Main Chat Section */}
        <div className="main-section">
          <div className="section-header">
            <h2>Ask Anything About Robotics</h2>
            <p>Powered by Gemini AI + Textbook RAG System</p>
          </div>
          
          <div className="chat-container-wrapper">
            <ChatBot />
          </div>
        </div>

        {/* Features Section */}
        <div className="features-section">
          <h3 className="features-title">✨ How It Works</h3>
          <div className="features-grid">
            <div className="feature-card">
              <div className="feature-icon">🔍</div>
              <h4>Retrieval</h4>
              <p>Searches through textbook content using TF-IDF similarity</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">🧠</div>
              <h4>Augmentation</h4>
              <p>Enhances queries with relevant context from chapters</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">💬</div>
              <h4>Generation</h4>
              <p>Generates accurate answers using Gemini AI</p>
            </div>
            <div className="feature-card">
              <div className="feature-icon">📚</div>
              <h4>Sources</h4>
              <p>Shows which textbook sections were referenced</p>
            </div>
          </div>
        </div>

        {/* Quick Questions */}
        <div className="quick-questions">
          <h3>💡 Try These Questions</h3>
          <div className="question-chips">
            {[
              "What is Physical AI?",
              "Explain ROS 2 nodes and topics",
              "How does Gazebo simulation work?",
              "What is NVIDIA Isaac Sim?",
              "How do humanoid robots maintain balance?",
              "What are VLA models in robotics?"
            ].map((question, idx) => (
              <button 
                key={idx}
                className="question-chip"
                onClick={() => {
                  // This will be handled by ChatBot component
                  window.dispatchEvent(new CustomEvent('set-question', { detail: question }));
                }}
              >
                {question}
              </button>
            ))}
          </div>
        </div>

        {/* Tech Stack */}
        <div className="tech-stack">
          <h3>⚙️ Tech Stack</h3>
          <div className="tech-icons">
            <div className="tech-item">
              <div className="tech-icon">⚛️</div>
              <span>React</span>
            </div>
            <div className="tech-item">
              <div className="tech-icon">🐍</div>
              <span>FastAPI</span>
            </div>
            <div className="tech-item">
              <div className="tech-icon">🤖</div>
              <span>Gemini AI</span>
            </div>
            <div className="tech-item">
              <div className="tech-icon">🔤</div>
              <span>TF-IDF</span>
            </div>
            <div className="tech-item">
              <div className="tech-icon">📘</div>
              <span>Docusaurus</span>
            </div>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default AskAIPage;