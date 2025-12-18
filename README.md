# Issa Compass - Self-Learning AI Assistant 🧭

A self-improving AI chatbot for visa consultation that learns from real consultant conversations. Built for the Vibe Hackathon.

## 🚀 Features

-   **Smart Response Generation**: AI generates human-like consultant responses based on conversation context
-   **Self-Learning System**: Automatically improves by comparing its responses to real consultant replies
-   **Prompt Evolution**: Tracks prompt changes over time in database
-   **Multiple LLM Support**: Works with Groq (Llama), Gemini, and OpenAI
-   **REST API**: Easy-to-use endpoints for integration

## 📁 Project Structure

```
├── app.py                  # Flask API server with all endpoints
├── ai_system.py           # Core self-learning AI logic
├── parse_conversations.py # Training data parser
├── llm_integration.py     # Multi-provider LLM client
├── database.py            # Supabase prompt storage
├── prompts.py             # System prompts (chatbot & editor)
├── config.py              # Configuration management
├── conversations.json     # Training data (128 examples)
├── requirements.txt       # Python dependencies
└── .env.example          # Environment variables template
```

## 🛠️ Setup Instructions

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

## 📡 API Endpoints

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

## 🚀 Deployment

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

## 🧪 Testing Examples

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

## 🎯 How Self-Learning Works

1. **AI generates a reply** to customer message
2. **Compare** AI reply vs real consultant reply
3. **Editor LLM analyzes** differences:
    - Tone mismatch?
    - Missing information?
    - Wrong format?
4. **Editor surgically updates** the main prompt
5. **Prompt saved to database** with version history
6. **Next reply uses improved prompt** 🔄

## 📊 Training Data

-   **15 conversations** with real customer-consultant exchanges
-   **128 training examples** extracted
-   Covers scenarios:
    -   Remote workers
    -   Freelancers
    -   Medical visitors
    -   Edge cases (visa rejections, document issues)

## 🔥 Advanced Features to Add (Reach A-Level)

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

## 🐛 Troubleshooting

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

## 📝 Notes

-   Uses Groq (Llama 3.1 70B) by default - very fast & free
-   Supabase free tier: 500MB database (more than enough)
-   All prompts are versioned and tracked
-   System is designed to improve continuously

## 🏆 Built for Vibe Hackathon

Created by [Your Name]
GitHub: [Your GitHub]
Deployed: [Your Railway/Render URL]

---

**Made with ⚡ using Cursor AI, Flask, Groq, and Supabase**
