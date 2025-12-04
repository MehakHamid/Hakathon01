import React, { useState } from 'react';
import Layout from '@theme/Layout';
import './styles.css';



function AskAIPage() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [sources, setSources] = useState([]);

  const API_URL = "http://localhost:8000"; // Change to your deployed URL

  const askQuestion = async () => {
    if (!question.trim()) {
      alert("Please enter a question");
      return;
    }

    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/ask?q=${encodeURIComponent(question)}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      setAnswer(data.answer);
      setSources(data.sources || []);
    } catch (error) {
      console.error("Error fetching answer:", error);
      setAnswer(`Error: Could not get answer. ${error.message}`);
      setSources([]);
    }
    setLoading(false);
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      askQuestion();
    }
  };

  return (
    <Layout title="Ask the AI Textbook" description="Chat with your Physical AI textbook">
      <div className="container">
        <h1>Ask the AI Textbook</h1>
        <p>Ask Questions from the Physical AI & Robotics Textbook</p>
        
        <div className="chat-container">
          <div className="input-area">
            <textarea
              value={question}
              onChange={(e) => setQuestion(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask a question from the textbook... (e.g., What is ROS 2?)"
              rows="3"
              disabled={loading}
            />
            <button 
              onClick={askQuestion} 
              disabled={loading}
              className="ask-button"
            >
              {loading ? 'Thinking...' : 'Ask AI'}
            </button>
          </div>

          {answer && (
            <div className="answer-area">
              <h3>🤖 Answer:</h3>
              <div className="answer-text">
                {answer.split('\n').map((line, idx) => (
                  <p key={idx}>{line}</p>
                ))}
              </div>
              
              {sources.length > 0 && (
                <div className="sources-area">
                  <h4>📚 Sources:</h4>
                  <ul>
                    {sources.map((source, idx) => (
                      <li key={idx}>{source}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}
        </div>

        <div className="example-questions">
          <h4>💡 Try these questions:</h4>
          <button className="example-btn" onClick={() => setQuestion("What is Physical AI?")}>
            What is Physical AI?
          </button>
          <button className="example-btn" onClick={() => setQuestion("Explain ROS 2")}>
            Explain ROS 2
          </button>
          <button className="example-btn" onClick={() => setQuestion("What is Gazebo?")}>
            What is Gazebo?
          </button>
        </div>
      </div>
    </Layout>
  );
}

export default AskAIPage;