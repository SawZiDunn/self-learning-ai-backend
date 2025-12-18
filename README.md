# Self-Learning AI Assistant for Visa Consultation

An intelligent chatbot system that learns from real consultant conversations to provide accurate visa consultation responses. The AI continuously improves itself by analyzing differences between its responses and actual consultant replies, automatically refining its behavior over time.

**Live Demo:** https://sawzidunn-hackathon.up.railway.app

## Overview

This system implements a self-improving AI assistant that:

-   Generates natural, human-like responses to visa consultation queries
-   Learns from real consultant conversations without manual intervention
-   Tracks and versions all improvements in a database
-   Supports multiple LLM providers for flexibility and reliability

## Core Capabilities

**Intelligent Response Generation**

-   Contextual understanding of multi-turn conversations
-   Natural language responses that match consultant communication style
-   Handles complex visa scenarios including eligibility, requirements, and procedures

**Autonomous Learning System**

-   Compares AI predictions with actual consultant responses
-   Identifies gaps in knowledge, tone, or format
-   Automatically updates system prompts based on analysis
-   Stores complete history of all improvements with reasoning

**Prompt Management**

-   Database-backed prompt versioning
-   Full audit trail of changes
-   Manual override capability for specific improvements
-   Performance tracking across iterations

**Multi-LLM Architecture**

-   Primary: Groq (Llama 3.3 70B) for speed and cost efficiency
-   Alternative: Google Gemini for redundancy
-   Optional: OpenAI GPT models
-   Easy provider switching without code changes

## Technology Stack

**Backend Framework**

-   Python 3.13
-   Flask 3.0.0 - Lightweight REST API server
-   Gunicorn - Production WSGI server

**AI/ML Integration**

-   Groq API - Primary LLM provider (Llama 3.3 70B)
-   Google Generative AI - Alternative provider (Gemini 1.5)
-   Custom prompt engineering for visa consultation domain

**Database & Storage**

-   Supabase (PostgreSQL) - Prompt versioning and history
-   JSON-based training data (15 real conversations, 128 examples)

**Development Tools**

-   python-dotenv - Environment configuration
-   httpx - Async HTTP client for LLM APIs
-   Cursor AI - Development assistant

**Deployment**

-   Railway.app - Cloud hosting platform
-   Docker - Containerization support
-   Git - Version control

## Architecture

```
├── app.py                  # Flask API server with 8 REST endpoints
├── ai_system.py           # Self-learning logic and training pipeline
├── llm_integration.py     # Multi-provider LLM abstraction layer
├── database.py            # Supabase client and prompt management
├── prompts.py             # System prompts (chatbot & editor)
├── parse_conversations.py # Training data extraction and formatting
├── config.py              # Configuration and validation
├── conversations.json     # Real consultant conversation data
└── requirements.txt       # Python dependencies
```

## Setup Instructions

### 1. Get API Keys (All FREE!)

**Groq API** (Recommended - fastest)

-   Sign up: https://console.groq.com
-   Get API key from dashboard
-   Free tier: Very generous limits

**Google Gemini** (Alternative)

-   Sign up: https://makersuite.google.com/app/apikey
-   Get API key
-   Free tier available

**Supabase Database** (Required)

-   Sign up: https://supabase.com
-   Create new project
-   Get URL and anon key from Settings → API

### 2. Clone & Install

```bash
cd issa-compass-assignment
cp .env.example .env
# Edit .env with your API keys
pip install -r requirements.txt
```

### 3. Initialize Database

Create this table in Supabase SQL Editor:

```sql
-- Create prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id SERIAL PRIMARY KEY,
    prompt_type VARCHAR(50) NOT NULL,
    prompt_text TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Create prompt_history table
CREATE TABLE IF NOT EXISTS prompt_history (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER REFERENCES prompts(id),
    old_prompt TEXT,
    new_prompt TEXT,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    performance_metrics JSONB
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_prompts_type ON prompts(prompt_type);
CREATE INDEX IF NOT EXISTS idx_prompts_updated ON prompts(updated_at DESC);
```

Then initialize with default prompts:

```bash
python3 -c "from database import init_database; init_database()"
```

### 4. Test the System

```bash
# Test conversation parser
python3 parse_conversations.py

# Test LLM integration
python3 llm_integration.py

# Test database
python3 database.py

# Test AI system
python3 ai_system.py
```

### 5. Run the Server

```bash
python3 app.py
```

Server runs on `http://localhost:5000`

## API Endpoints

### 1. Generate AI Reply

```bash
curl -X POST http://localhost:5000/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I am American and currently in Bali. Can I apply from Indonesia?",
    "chatHistory": [
      {"role": "consultant", "message": "Hi there! The DTV is perfect for remote workers."},
      {"role": "client", "message": "Hello, I am interested in the DTV visa."}
    ]
  }'
```

**Response:**

```json
{
    "aiReply": "Yes, absolutely! As a US citizen, you can apply for the DTV at the Thai Embassy in Jakarta...",
    "provider": "groq"
}
```

### 2. Auto-Improve AI (Self-Learning)

```bash
curl -X POST http://localhost:5000/improve-ai \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "What documents do I need?",
    "chatHistory": [],
    "consultantReply": "You will need: 1) Valid passport 2) Bank statements 3) Employment letter"
  }'
```

**Response:**

```json
{
    "predictedReply": "For the DTV visa, you need...",
    "actualReply": "You will need: 1) Valid passport...",
    "analysis": "AI response was too verbose. Real consultant used numbered list.",
    "changesMade": [
        "Added instruction to use numbered lists for document requirements",
        "Shortened response length guideline"
    ],
    "updatedPrompt": "Updated system prompt..."
}
```

### 3. Manual Prompt Improvement

```bash
curl -X POST http://localhost:5000/improve-ai-manually \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Be more concise. Always mention appointment booking proactively."
  }'
```

### 4. Get Current Prompt

```bash
curl http://localhost:5000/prompt
```

### 5. Get Prompt History

```bash
curl http://localhost:5000/prompt-history?limit=10
```

### 6. Train on Sample Data

```bash
curl -X POST http://localhost:5000/train \
  -H "Content-Type: application/json" \
  -d '{"numSamples": 5}'
```

## Deployment

### Deploy to Railway (Easiest)

1. Create account at https://railway.app
2. Click "New Project" → "Deploy from GitHub"
3. Connect your repository
4. Add environment variables in Railway dashboard
5. Railway auto-deploys!

Your URL: `https://[your-project].up.railway.app`

### Deploy to Render

1. Create account at https://render.com
2. New → Web Service
3. Connect GitHub repo
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `gunicorn app:app`
6. Add environment variables
7. Deploy!

### Environment Variables for Production

```
GROQ_API_KEY=your_key
SUPABASE_URL=your_url
SUPABASE_KEY=your_key
LLM_PROVIDER=groq
PORT=5000
```

## Testing Examples

### Test Conversation Flow

```bash
# 1. Generate initial reply
curl -X POST http://localhost:5000/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I work remotely for a US company. Can I get a DTV visa?",
    "chatHistory": []
  }'

# 2. Continue conversation
curl -X POST http://localhost:5000/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "What documents do I need?",
    "chatHistory": [
      {"role": "client", "message": "I work remotely for a US company. Can I get a DTV visa?"},
      {"role": "consultant", "message": "Yes! The DTV is perfect for remote workers..."}
    ]
  }'
```

### Train the AI

```bash
# Train on 10 real conversations
curl -X POST http://localhost:5000/train \
  -H "Content-Type: application/json" \
  -d '{"numSamples": 10}'
```

## How the Self-Learning System Works

The AI improves itself through a continuous feedback loop:

**1. Response Generation Phase**

```
Client Question → Current Prompt → LLM → AI Response
```

The system retrieves the latest prompt from the database and uses it to generate a response based on conversation context.

**2. Comparison Phase**

```
AI Response + Real Consultant Response → Analysis
```

When training data is available, the system compares what the AI would say versus what a real consultant actually said.

**3. Analysis Phase**

```
Editor LLM → Identifies Gaps → Generates Improvements
```

A separate "editor" LLM analyzes differences:

-   Tone and style mismatches
-   Missing critical information
-   Incorrect formatting or structure
-   Logic errors or inaccuracies

**4. Update Phase**

```
Improved Prompt → Database → Version History
```

The editor surgically updates specific parts of the prompt with precise changes, then stores it with full audit trail.

**5. Iteration**

```
Next Request → Uses Improved Prompt → Better Response
```

All subsequent requests automatically use the improved prompt, making the system continuously better.

## AI Integration Approach

**Dual-LLM Architecture**

I implemented a unique two-model system:

1. **Main Chatbot LLM** - Responds to customer queries

    - Uses detailed system prompt with visa knowledge
    - Formatted to match consultant communication style
    - Returns JSON-structured responses for easy parsing

2. **Editor LLM** - Analyzes and improves the chatbot
    - Receives both AI and real responses
    - Identifies specific areas needing improvement
    - Updates prompts with surgical precision
    - Documents reasoning for each change

**Why This Works**

Traditional chatbots are static - they only work as well as their initial prompt. This system:

-   Learns from real interactions without manual retraining
-   Preserves successful behaviors while fixing problems
-   Maintains full transparency of all changes
-   Scales knowledge automatically as more data becomes available

**Training Data Processing**

The system parses real conversation logs to extract:

-   Client message sequences (single or multiple messages)
-   Full conversation history up to that point
-   Actual consultant responses
-   Context about visa type and situation

This creates supervised learning examples that drive improvements.

## Implementation Details

**Prompt Engineering**

-   Base prompt covers Thai DTV visa knowledge, eligibility, process
-   Includes response style guidelines (concise, friendly, professional)
-   Structured to output JSON for reliable parsing
-   Editor prompt focuses on gap analysis and surgical updates
    What I Built

**Core Innovation: Self-Improving AI Without Manual Training**

Rather than building a static chatbot that requires constant manual updates, I created a system that learns autonomously. The key insight was using a second LLM as a "critic" that analyzes the main chatbot's performance and makes targeted improvements to its behavior.

**Technical Achievements:**

1. Designed a dual-LLM architecture where models work together
2. Implemented automatic prompt versioning with full audit trails
3. Created a training pipeline that processes real conversation data
4. Built a multi-provider LLM system for reliability and cost optimization
5. Deployed production-ready API with 8 functional endpoints
6. Integrated PostgreSQL database for persistent prompt storage
7. Wrote comprehensive error handling and fallback mechanisms

**Why This Approach Is Effective:**

Traditional ML requires labeled datasets, model training infrastructure, and specialized expertise. This system achieves similar results using:

-   Prompt engineering instead of model fine-tuning
-   LLM-as-judge for quality assessment
-   Incremental improvements rather than batch retraining
-   Zero infrastructure beyond API calls and a database

The result is a system that gets smarter with every conversation it processes, without requiring data scientists or expensive compute resources.

## Testing

See [TEST_COMMANDS.md](TEST_COMMANDS.md) for complete API testing examples.

Quick test:

```bash
curl https://sawzidunn-hackathon.up.railway.app/
```

## Built for Vibe Hackathon

**Repository:** https://github.com/sawzidunn/self-learning-ai-assistant  
**Live Server:** https://sawzidunn-hackathon.up.railway.app  
**Documentation:** TEST_COMMANDS.md, DEPLOYMENT_STATUS.md

Created using Cursor AI, Flask, Groq, and Supabase

-   Provider switching if one LLM service fails
-   Comprehensive logging for debugging

**API Design**

-   RESTful endpoints following standard conventions
-   JSON request/response format
-   Clear error messages with HTTP status codes
-   CORS-ready for frontend integration

## Future Enhancements

1. **Frontend Dashboard** (Next.js)

    - Visualize conversations
    - Show prompt evolution diff
    - Real-time testing interface

2. **Docker Deployment**

    ```dockerfile
    FROM python:3.11-slim
    WORKDIR /app
    COPY . .
    RUN pip install -r requirements.txt
    CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
    ```

3. **Performance Metrics**

    - Track response quality scores
    - A/B test different prompts
    - Analytics dashboard

4. **Multi-turn Conversation Support**

    - Session management
    - Context window optimization

5. **RAG Integration**
    - Vector database for visa knowledge
    - Semantic search for similar cases

## Troubleshooting

**Error: "Supabase client not initialized"**

-   Check SUPABASE_URL and SUPABASE_KEY in .env
-   Run database initialization script

**Error: "Groq client not initialized"**

-   Check GROQ_API_KEY in .env
-   Try switching to Gemini: `LLM_PROVIDER=gemini`

**JSON Parsing Errors**

-   LLM sometimes returns non-JSON
-   System has fallback handling
-   Try different provider or adjust temperature

## Notes

-   Uses Groq (Llama 3.1 70B) by default - very fast & free
-   Supabase free tier: 500MB database (more than enough)
-   All prompts are versioned and tracked
-   System is designed to improve continuously

## 🏆 Built for Vibe Hackathon

Created by Saw Zi Dunn
GitHub: https://github.com/SawZiDunn/self-learning-ai-backend
Deployed: https://sawzidunn-hackathon.up.railway.app

---

**Made with ⚡ using Cursor AI, Flask, Groq, and Supabase**
