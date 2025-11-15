import React from 'react';
import { Link } from 'react-router-dom';

const Landing: React.FC = () => {
  return (
    <div className="landing-page">
      {/* Hero Section */}
      <section className="hero-section hero-bg relative overflow-hidden">
        {/* Animated Background Elements */}
        <div className="floating-orbs">
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
          <div className="orb orb-3"></div>
          <div className="orb orb-4"></div>
        </div>

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="hero-content text-center">
            <div className="hero-badge">
              <span className="badge-text">🇮🇳 Made for Indian MSMEs</span>
            </div>
            
            <h1 className="hero-title">
              Your <span className="text-gradient">AI-Powered</span> Digital Partner
            </h1>
            
            <p className="hero-subtitle">
              To empower every Indian MSME with an intelligent digital partner that<br />
              simplifies business operations, automates compliance, and accelerates growth
            </p>

            <div className="hero-buttons">
              <Link to="/register" className="btn-hero-primary">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                Get Started Free
              </Link>
              <Link to="/login" className="btn-hero-secondary">
                <svg className="w-5 h-5 mr-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M14 5l7 7m0 0l-7 7m7-7H3" />
                </svg>
                Sign In
              </Link>
            </div>

            <div className="hero-stats">
              <div className="stat-item">
                <div className="stat-number">10,000+</div>
                <div className="stat-label">MSMEs Trust Us</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">₹500Cr+</div>
                <div className="stat-label">Invoices Generated</div>
              </div>
              <div className="stat-item">
                <div className="stat-number">99.9%</div>
                <div className="stat-label">GST Compliance</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Mission Section */}
      <section className="mission-section">
        <div className="container mx-auto px-4 py-20">
          <div className="section-header">
            <span className="section-badge">🚀 Our Mission</span>
            <h2 className="section-title">Bridging the Technology Gap</h2>
            <p className="section-subtitle">
              Our mission is to bridge the technology gap for small and medium businesses by<br />
              delivering an AI-driven platform that transforms how you do business
            </p>
          </div>

          <div className="mission-grid">
            <div className="mission-card">
              <div className="mission-icon automation">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 3v2m6-2v2M9 19v2m6-2v2M5 9H3m2 6H3m18-6h-2m2 6h-2M7 19h10a2 2 0 002-2V7a2 2 0 00-2-2H7a2 2 0 00-2 2v10a2 2 0 002 2zM9 9h6v6H9V9z" />
                </svg>
              </div>
              <h3 className="mission-card-title">Automate Daily Workflows</h3>
              <p className="mission-card-text">
                Streamline billing, GST filing, and compliance with intelligent automation. 
                Say goodbye to manual data entry and paperwork.
              </p>
              <ul className="mission-list">
                <li>✓ Automatic invoice generation</li>
                <li>✓ Real-time GST calculations</li>
                <li>✓ One-click compliance reports</li>
              </ul>
            </div>

            <div className="mission-card">
              <div className="mission-icon insights">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                </svg>
              </div>
              <h3 className="mission-card-title">Real-Time Insights</h3>
              <p className="mission-card-text">
                Get instant financial insights with multilingual support. Understand your 
                business better with AI-powered analytics.
              </p>
              <ul className="mission-list">
                <li>✓ Live dashboard analytics</li>
                <li>✓ Support in 10+ languages</li>
                <li>✓ Smart financial forecasting</li>
              </ul>
            </div>

            <div className="mission-card">
              <div className="mission-icon security">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
                </svg>
              </div>
              <h3 className="mission-card-title">India-First Security</h3>
              <p className="mission-card-text">
                Your data stays in India with bank-grade encryption. We ensure complete 
                privacy and security for your business information.
              </p>
              <ul className="mission-list">
                <li>✓ 256-bit encryption</li>
                <li>✓ India-based servers</li>
                <li>✓ GDPR compliant</li>
              </ul>
            </div>

            <div className="mission-card">
              <div className="mission-icon schemes">
                <svg fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                </svg>
              </div>
              <h3 className="mission-card-title">Government Schemes</h3>
              <p className="mission-card-text">
                Discover and benefit from government schemes seamlessly. Get personalized 
                recommendations for subsidies and support programs.
              </p>
              <ul className="mission-list">
                <li>✓ Scheme recommendations</li>
                <li>✓ Automated application help</li>
                <li>✓ Eligibility tracking</li>
              </ul>
            </div>
          </div>
        </div>
      </section>

      {/* Vision Section */}
      <section className="vision-section">
        <div className="container mx-auto px-4 py-20">
          <div className="vision-content">
            <div className="vision-text">
              <span className="section-badge">💡 Our Vision</span>
              <h2 className="section-title-left">Business Management as Simple as Conversation</h2>
              <p className="vision-description">
                SmartBiz AI aims to make business management as simple as having a conversation — 
                <span className="highlight"> your business, managed by AI.</span>
              </p>
              <p className="vision-description">
                No complex software. No steep learning curve. Just chat with your AI assistant 
                and let it handle the rest. From generating invoices to filing GST returns, 
                everything happens through natural conversation.
              </p>
              <div className="vision-features">
                <div className="vision-feature-item">
                  <span className="feature-icon">💬</span>
                  <span>Conversational Interface</span>
                </div>
                <div className="vision-feature-item">
                  <span className="feature-icon">🤖</span>
                  <span>AI-Powered Automation</span>
                </div>
                <div className="vision-feature-item">
                  <span className="feature-icon">📱</span>
                  <span>Mobile-First Design</span>
                </div>
                <div className="vision-feature-item">
                  <span className="feature-icon">🌐</span>
                  <span>Multi-Language Support</span>
                </div>
              </div>
            </div>
            <div className="vision-image">
              <div className="floating-card card-1">
                <div className="card-icon">📊</div>
                <div className="card-title">Real-Time Analytics</div>
              </div>
              <div className="floating-card card-2">
                <div className="card-icon">🧾</div>
                <div className="card-title">Smart Invoicing</div>
              </div>
              <div className="floating-card card-3">
                <div className="card-icon">📈</div>
                <div className="card-title">Growth Insights</div>
              </div>
              <div className="floating-card card-4">
                <div className="card-icon">✅</div>
                <div className="card-title">GST Compliance</div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="cta-section cta-bg relative overflow-hidden">
        <div className="floating-orbs">
          <div className="orb orb-1"></div>
          <div className="orb orb-2"></div>
        </div>

        <div className="container mx-auto px-4 py-20 relative z-10">
          <div className="cta-content">
            <h2 className="cta-title">Ready to Transform Your Business?</h2>
            <p className="cta-subtitle">
              Join thousands of Indian MSMEs already growing with SmartBiz AI
            </p>
            <div className="cta-buttons">
              <Link to="/register" className="btn-cta-primary">
                Start Free Trial
                <svg className="w-5 h-5 ml-2" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
              <a href="#features" className="btn-cta-secondary">
                Learn More
              </a>
            </div>
            <p className="cta-note">
              ✨ No credit card required • 14-day free trial • Cancel anytime
            </p>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer-section">
        <div className="container mx-auto px-4 py-12">
          <div className="footer-content">
            <div className="footer-brand">
              <div className="footer-logo">
                <svg className="w-10 h-10 text-cyan-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                </svg>
                <span className="footer-logo-text">SmartBiz AI</span>
              </div>
              <p className="footer-tagline">
                Your AI-powered business co-pilot for the digital age
              </p>
            </div>
            <div className="footer-links">
              <div className="footer-column">
                <h4 className="footer-column-title">Product</h4>
                <ul className="footer-list">
                  <li><a href="#features">Features</a></li>
                  <li><a href="#pricing">Pricing</a></li>
                  <li><a href="#integrations">Integrations</a></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4 className="footer-column-title">Company</h4>
                <ul className="footer-list">
                  <li><a href="#about">About Us</a></li>
                  <li><a href="#contact">Contact</a></li>
                  <li><a href="#careers">Careers</a></li>
                </ul>
              </div>
              <div className="footer-column">
                <h4 className="footer-column-title">Legal</h4>
                <ul className="footer-list">
                  <li><a href="#privacy">Privacy Policy</a></li>
                  <li><a href="#terms">Terms of Service</a></li>
                  <li><a href="#security">Security</a></li>
                </ul>
              </div>
            </div>
          </div>
          <div className="footer-bottom">
            <p className="footer-copyright">
              © 2025 SmartBiz AI. Made with ❤️ in India for Indian MSMEs
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Landing;
