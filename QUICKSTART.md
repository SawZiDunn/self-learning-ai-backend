# Quick Start Guide 🚀

Follow these steps to get up and running in minutes!

## 1️⃣ Get Your API Keys (5 minutes)

### Groq (Fastest, Recommended)

1. Go to: https://console.groq.com
2. Sign up with Google/GitHub
3. Click "API Keys" → "Create API Key"
4. Copy the key (starts with `gsk_...`)

### Supabase (Database)

1. Go to: https://supabase.com
2. Sign up and create a new project
3. Wait 2 minutes for project to initialize
4. Go to Settings → API
5. Copy:
    - Project URL
    - `anon` `public` key

## 2️⃣ Set Up Environment

```bash
cd issa-compass-assignment

# Create .env file
cp .env.example .env

# Edit .env and paste your keys:
# GROQ_API_KEY=gsk_...
# SUPABASE_URL=https://...supabase.co
# SUPABASE_KEY=eyJ...
```

## 3️⃣ Install & Initialize

```bash
# Install dependencies
pip install -r requirements.txt

# Initialize database
python3 -c "from database import init_database; init_database()"
```

## 4️⃣ Test It!

```bash
# Start the server
python3 app.py
```

Visit: http://localhost:5000

## 5️⃣ Try the API

```bash
# Test generation
curl -X POST http://localhost:5000/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I need help with DTV visa",
    "chatHistory": []
  }'

# Train the AI
curl -X POST http://localhost:5000/train \
  -H "Content-Type: application/json" \
  -d '{"numSamples": 3}'
```

## 6️⃣ Deploy to Railway

1. Create account: https://railway.app
2. Click "New Project"
3. Select "Deploy from GitHub"
4. Choose this repository
5. Add environment variables:
    - `GROQ_API_KEY`
    - `SUPABASE_URL`
    - `SUPABASE_KEY`
6. Deploy! 🚀

Your API will be live at: `https://your-project.up.railway.app`

## 🎉 You're Done!

Now you have:

-   ✅ Working AI chatbot
-   ✅ Self-learning system
-   ✅ REST API
-   ✅ Deployed to production

## Next Steps

-   Read [README.md](README.md) for full documentation
-   Test all endpoints
-   Train on more data
-   Add your own features!

## Need Help?

Common issues:

-   **"Client not initialized"**: Check your API keys in .env
-   **Database error**: Run the database initialization again
-   **Import errors**: Run `pip install -r requirements.txt`

Happy coding! 🧭
