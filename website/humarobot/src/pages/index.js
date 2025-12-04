import React from 'react';
import Layout from '@theme/Layout';
import Link from '@docusaurus/Link';

function Home() {
  return (
    <Layout title="Home" description="Physical AI & Humanoid Robotics Textbook">
      <div style={{
        padding: '4rem 1rem',
        textAlign: 'center',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        color: 'white'
      }}>
        <h1 style={{fontSize: '3rem', marginBottom: '1rem'}}>
          🤖 Physical AI & Humanoid Robotics
        </h1>
        <p style={{fontSize: '1.5rem', maxWidth: '800px', margin: '0 auto 2rem'}}>
          Learn to build intelligent robots with AI that interacts with the physical world
        </p>
        <div style={{display: 'flex', gap: '1rem', justifyContent: 'center'}}>
          <Link
            className="button button--primary button--lg"
            to="/docs/intro">
            Start Learning →
          </Link>
          <Link
            className="button button--secondary button--lg"
            to="/askai">
            Ask AI Assistant
          </Link>
        </div>
      </div>

      {/* Features Section */}
      <div style={{padding: '4rem 2rem', maxWidth: '1200px', margin: '0 auto'}}>
        <h2 style={{textAlign: 'center', marginBottom: '3rem'}}>What You'll Learn</h2>
        <div style={{display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '2rem'}}>
          <div style={{padding: '2rem', border: '1px solid #e5e7eb', borderRadius: '10px'}}>
            <h3>🤖 ROS 2 Fundamentals</h3>
            <p>Master the Robot Operating System - the nervous system of modern robots.</p>
          </div>
          <div style={{padding: '2rem', border: '1px solid #e5e7eb', borderRadius: '10px'}}>
            <h3>🎮 Gazebo Simulation</h3>
            <p>Create digital twins and test robots in virtual environments.</p>
          </div>
          <div style={{padding: '2rem', border: '1px solid #e5e7eb', borderRadius: '10px'}}>
            <h3>🧠 NVIDIA Isaac AI</h3>
            <p>Implement AI-powered perception and manipulation.</p>
          </div>
          <div style={{padding: '2rem', border: '1px solid #e5e7eb', borderRadius: '10px'}}>
            <h3>🗣️ Conversational Robotics</h3>
            <p>Integrate GPT models for natural robot interaction.</p>
          </div>
        </div>
      </div>
    </Layout>
  );
}

export default Home;