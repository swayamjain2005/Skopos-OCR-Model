import React from 'react';
import { useNavigate } from 'react-router-dom';
import { FileText, Scan, Brain, Code, ArrowRight, Zap, Shield, Layers, CheckCircle, ChevronRight, Globe, Database, Lock, FileJson, Wand2 } from 'lucide-react';
import './LandingPage.css';

const LandingPage = () => {
    const navigate = useNavigate();

    return (
        <div className="landing-page">
            <nav className="navbar">
                <div className="logo">
                    <div className="logo-icon-bg">
                        <Scan className="logo-icon" size={24} />
                    </div>
                    <span className="logo-text">Skopos OCR</span>
                </div>
                <div className="nav-links">
                    <a href="#features">Features</a>
                    <a href="#workflow">How it Works</a>
                </div>
                <div className="nav-buttons">
                    <button className="btn-primary" onClick={() => navigate('/app')}>Launch App <ArrowRight size={16} /></button>
                </div>
            </nav>

            <header className="hero">
                <div className="hero-content">
                    <h1>
                        Transform Static Documents <br />
                        Into <span className="highlight-text">Dynamic HTML</span> Instantly
                    </h1>
                    <p className="hero-sub">
                        Skopos combines advanced computer vision with Generative AI to digitize, format, and edit your documents with unprecedented accuracy.
                    </p>
                    <div className="hero-buttons">
                        <button className="btn-primary glow" onClick={() => navigate('/app')}>Start Converting <ArrowRight size={16} /></button>
                    </div>

                    <div className="hero-logos">
                        <span>Powered by State-of-the-Art AI</span>
                        <div className="logo-list">
                            <span className="tech-logo"><Brain size={18} /> Gemini Pro</span>
                            <span className="tech-logo"><Scan size={18} /> Florence-2 OCR</span>
                            <span className="tech-logo"><Zap size={18} /> Fast API</span>
                        </div>
                    </div>
                </div>

                <div className="hero-visual-container">
                    <div className="central-hub">
                        <div className="hub-core">
                            <Scan size={48} color="#2563eb" />
                            <span>OCR Core</span>
                        </div>
                        {/* Orbiting Nodes */}
                        <div className="orbit-node node-1"><FileText size={20} /></div>
                        <div className="orbit-node node-2"><FileJson size={20} /></div>
                        <div className="orbit-node node-3"><Code size={20} /></div>
                        <div className="orbit-node node-4"><Wand2 size={20} /></div>
                    </div>

                    <div className="floating-card card-right">
                        <div className="card-icon"><CheckCircle size={16} color="green" /></div>
                        <div className="card-text">
                            <strong>Smart Formatting</strong>
                            <span>Recreates tables & layouts perfectly.</span>
                        </div>
                    </div>

                    <div className="floating-card card-left">
                        <div className="card-icon"><Wand2 size={16} color="purple" /></div>
                        <div className="card-text">
                            <strong>AI Editing</strong>
                            <span>"Make headings bold" - Done.</span>
                        </div>
                    </div>
                </div>
            </header>

            <section className="features-section" id="features">
                <div className="section-header">
                    <span className="badge">| CAPABILITIES |</span>
                    <h2>Intelligent Document <br /> Processing Pipeline</h2>
                </div>

                <div className="features-grid">
                    <div className="feature-card large">
                        <div className="card-content">
                            <h3>Advanced Vision Models</h3>
                            <p>Utilizing Microsoft's Florence-2 model to extract text with high precision, even from complex scanned documents and images.</p>
                        </div>
                        <div className="card-visual-center">
                            <div className="model-icon"><Scan size={40} /></div>
                        </div>
                    </div>

                    <div className="feature-card">
                        <div className="card-icon-top"><Wand2 size={32} color="#2563eb" /></div>
                        <h3>Generative Formatting</h3>
                        <p>Gemini AI analyzes raw text to reconstruct semantic HTML structure, preserving tables, lists, and headers.</p>
                    </div>

                    <div className="feature-card">
                        <div className="card-header-row">
                            <span className="tag">Interactive</span>
                            <span className="tag">Real-time</span>
                        </div>
                        <h3>Natural Language Editing</h3>
                        <p>Chat with your document to make changes. No coding required.</p>
                        <div className="input-mock">
                            <span>"Change the font to Arial..."</span>
                            <ArrowRight size={14} />
                        </div>
                    </div>
                </div>
            </section>

            <section className="agents-section" id="workflow">
                <div className="section-header">
                    <span className="badge">| WORKFLOW |</span>
                    <h2>From Image to HTML <br /> In Seconds</h2>
                </div>

                <div className="agents-visual">
                    <div className="agent-tree">
                        <div className="tree-node root"><div className="node-circle main"><Layers size={24} /></div><span>Upload</span></div>
                        <div className="tree-branch"></div>
                        <div className="tree-node leaf leaf-1">
                            <div className="leaf-card">
                                <div className="leaf-icon"><Scan size={16} /></div>
                                <strong>Extraction</strong>
                                <p>Florence-2 reads the raw pixel data.</p>
                            </div>
                        </div>
                        <div className="tree-node leaf leaf-2">
                            <div className="leaf-card">
                                <div className="leaf-icon"><Code size={16} /></div>
                                <strong>Generation</strong>
                                <p>Gemini structures it into clean code.</p>
                            </div>
                        </div>
                    </div>
                    <button className="btn-primary small-pill" onClick={() => navigate('/app')}>Try It Now <ChevronRight size={14} /></button>
                </div>
            </section>

            <footer className="footer">
                <div className="footer-content">
                    <div className="footer-col">
                        <div className="logo">
                            <Scan size={20} /> <span>Skopos OCR</span>
                        </div>
                        <p>Next-generation document digitization.</p>
                    </div>
                    <div className="footer-col">
                        <h4>Product</h4>
                        <a href="#features">Features</a>
                        <a href="#workflow">Workflow</a>
                    </div>
                    <div className="footer-col">
                        <h4>Technology</h4>
                        <a href="#">Florence-2</a>
                        <a href="#">Gemini Pro</a>
                    </div>
                </div>
                <div className="footer-bottom">
                    <p>© 2024 Skopos OCR. All rights reserved.</p>
                </div>
            </footer>
        </div>
    );
};

export default LandingPage;
