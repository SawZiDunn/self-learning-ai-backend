# API Test Commands - Self-Learning AI Assistant

## Production Server
Base URL: https://sawzidunn-hackathon.up.railway.app

## Quick Start - Test All Endpoints

### 1. Health Check
```bash
curl https://sawzidunn-hackathon.up.railway.app/
curl https://sawzidunn-hackathon.up.railway.app/health
```

### 2. Generate AI Reply
```bash
curl -X POST https://sawzidunn-hackathon.up.railway.app/generate-reply \
  -H "Content-Type: application/json" \
  -d '{"clientSequence": "I am American and currently in Bali. Can I apply from Indonesia?", "chatHistory": [{"role": "consultant", "message": "Hi there! Thank you for reaching out. The DTV is perfect for remote workers like yourself. May I know your nationality and which country you would like to apply from?"}, {"role": "client", "message": "Hello, I am interested in the DTV visa for Thailand. I work remotely as a software developer for a US company."}]}'
```

### 3. Auto-Improve AI
```bash
curl -X POST https://sawzidunn-hackathon.up.railway.app/improve-ai \
  -H "Content-Type: application/json" \
  -d '{"clientSequence": "How much does it cost?", "chatHistory": [], "consultantReply": "The government fee is 10,000 THB. Our service fee for remote workers is typically 18,000 THB total, which includes everything - document review, application submission, and support throughout the process."}'
```

### 4. Manually Improve AI
```bash
curl -X POST https://sawzidunn-hackathon.up.railway.app/improve-ai-manually \
  -H "Content-Type: application/json" \
  -d '{"instructions": "Be more concise. Always mention appointment booking proactively."}'
```

### 5. Get Current Prompt
```bash
curl https://sawzidunn-hackathon.up.railway.app/prompt
```

### 6. Get Prompt History
```bash
curl https://sawzidunn-hackathon.up.railway.app/prompt-history?limit=5
```

### 7. Train on Sample Data
```bash
curl -X POST https://sawzidunn-hackathon.up.railway.app/train \
  -H "Content-Type: application/json" \
  -d '{"numSamples": 3}'
```

## Additional Examples

### Simple Question
```bash
curl -X POST https://sawzidunn-hackathon.up.railway.app/generate-reply \
  -H "Content-Type: application/json" \
  -d '{"clientSequence": "What documents do I need for DTV?", "chatHistory": []}'
```

### Follow-up Question with Context
```bash
curl -X POST https://sawzidunn-hackathon.up.railway.app/generate-reply \
  -H "Content-Type: application/json" \
  -d '{"clientSequence": "How long does the processing take?", "chatHistory": [{"role": "client", "message": "What documents do I need for DTV?"}, {"role": "consultant", "message": "You will need: valid passport (6+ months validity), bank statements (3 months showing 500k THB), employment verification, proof of income, passport photo, and proof of address in your application country."}]}'
```

## Notes
- All endpoints return JSON responses
- The self-learning system automatically improves from real conversation data
- Training endpoint processes sample conversations to refine AI responses
- Prompt history tracks all improvements over time
