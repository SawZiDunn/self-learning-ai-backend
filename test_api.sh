# Example cURL Commands for Testing Issa Compass API

# Replace YOUR_URL with your deployed URL, e.g.:
# LOCAL: http://localhost:5000
# RAILWAY: https://your-project.up.railway.app
# RENDER: https://your-project.onrender.com

URL="http://localhost:5000"

echo "======================================"
echo "Issa Compass API - Example Commands"
echo "======================================"
echo ""

# 1. Health Check
echo "1. Health Check:"
echo "curl $URL/health"
echo ""
curl $URL/health
echo -e "\n"

# 2. Get API Info
echo "2. Get API Info:"
echo "curl $URL/"
echo ""
curl $URL/
echo -e "\n\n"

# 3. Generate AI Reply (Simple)
echo "3. Generate AI Reply (Simple):"
cat <<'EOF'
curl -X POST $URL/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I am interested in the DTV visa. I work remotely as a software developer.",
    "chatHistory": []
  }'
EOF
echo ""
curl -X POST $URL/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I am interested in the DTV visa. I work remotely as a software developer.",
    "chatHistory": []
  }'
echo -e "\n\n"

# 4. Generate AI Reply (With Chat History)
echo "4. Generate AI Reply (With Chat History):"
cat <<'EOF'
curl -X POST $URL/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "What documents do I need to prepare?",
    "chatHistory": [
      {"role": "client", "message": "I am interested in the DTV visa."},
      {"role": "consultant", "message": "Hi! The DTV is perfect for remote workers. May I know your nationality?"},
      {"role": "client", "message": "I am American, currently in Bali."}
    ]
  }'
EOF
echo ""
curl -X POST $URL/generate-reply \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "What documents do I need to prepare?",
    "chatHistory": [
      {"role": "client", "message": "I am interested in the DTV visa."},
      {"role": "consultant", "message": "Hi! The DTV is perfect for remote workers. May I know your nationality?"},
      {"role": "client", "message": "I am American, currently in Bali."}
    ]
  }'
echo -e "\n\n"

# 5. Auto-Improve AI (Self-Learning)
echo "5. Auto-Improve AI (Self-Learning):"
cat <<'EOF'
curl -X POST $URL/improve-ai \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I am American and currently in Bali. Can I apply from Indonesia?",
    "chatHistory": [
      {"role": "client", "message": "Hello, I am interested in the DTV visa."},
      {"role": "consultant", "message": "Hi! The DTV is perfect for remote workers."}
    ],
    "consultantReply": "Yes, you can apply from Indonesia! Our service fees are 18,000 THB including government fees. Processing takes about 10 business days."
  }'
EOF
echo ""
curl -X POST $URL/improve-ai \
  -H "Content-Type: application/json" \
  -d '{
    "clientSequence": "I am American and currently in Bali. Can I apply from Indonesia?",
    "chatHistory": [
      {"role": "client", "message": "Hello, I am interested in the DTV visa."},
      {"role": "consultant", "message": "Hi! The DTV is perfect for remote workers."}
    ],
    "consultantReply": "Yes, you can apply from Indonesia! Our service fees are 18,000 THB including government fees. Processing takes about 10 business days."
  }'
echo -e "\n\n"

# 6. Manually Improve Prompt
echo "6. Manually Improve Prompt:"
cat <<'EOF'
curl -X POST $URL/improve-ai-manually \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Be more concise. Use bullet points for lists. Always mention appointment booking proactively."
  }'
EOF
echo ""
curl -X POST $URL/improve-ai-manually \
  -H "Content-Type: application/json" \
  -d '{
    "instructions": "Be more concise. Use bullet points for lists. Always mention appointment booking proactively."
  }'
echo -e "\n\n"

# 7. Get Current Prompt
echo "7. Get Current Prompt:"
echo "curl $URL/prompt"
echo ""
curl $URL/prompt | python3 -m json.tool 2>/dev/null || curl $URL/prompt
echo -e "\n\n"

# 8. Get Prompt History
echo "8. Get Prompt History:"
echo "curl '$URL/prompt-history?limit=5'"
echo ""
curl "$URL/prompt-history?limit=5" | python3 -m json.tool 2>/dev/null || curl "$URL/prompt-history?limit=5"
echo -e "\n\n"

# 9. Train on Sample Data
echo "9. Train on Sample Data (3 samples):"
cat <<'EOF'
curl -X POST $URL/train \
  -H "Content-Type: application/json" \
  -d '{"numSamples": 3}'
EOF
echo ""
echo "(This will take 1-2 minutes depending on LLM speed)"
# Uncomment to actually run training:
# curl -X POST $URL/train -H "Content-Type: application/json" -d '{"numSamples": 3}'
echo -e "\n\n"

echo "======================================"
echo "All example commands shown above!"
echo "======================================"
