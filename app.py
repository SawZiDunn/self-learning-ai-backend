from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
from ai_system import (
    generate_ai_reply,
    improve_prompt_with_editor,
    manually_improve_prompt,
    train_on_sample_data
)
from llm_integration import format_client_sequence, format_consultant_reply
from database import get_prompt, get_prompt_history

load_dotenv()

app = Flask(__name__)

# Determine which LLM provider to use
LLM_PROVIDER = os.getenv('LLM_PROVIDER', 'groq')  # Default to groq


@app.route('/')
def index():
    return jsonify({
        "message": "Issa Compass Self-Learning AI Assistant 🧭",
        "status": "running",
        "version": "1.0.0",
        "llm_provider": LLM_PROVIDER,
        "endpoints": {
            "POST /generate-reply": "Generate an AI response based on conversation context",
            "POST /improve-ai": "Auto-improve the AI prompt by comparing predicted vs actual",
            "POST /improve-ai-manually": "Manually update the AI prompt with specific instructions",
            "GET /prompt": "Get current chatbot prompt",
            "GET /prompt-history": "Get prompt change history",
            "POST /train": "Train AI on sample data"
        }
    })


@app.route('/health')
def health():
    return jsonify({"status": "healthy"})


@app.route('/generate-reply', methods=['POST'])
def generate_reply():
    """
    Generate an AI response based on conversation context.
    
    Request:
    {
      "clientSequence": "I'm American and currently in Bali. Can I apply from Indonesia?",
      "chatHistory": [
        { "role": "consultant", "message": "Hi there! ..." },
        { "role": "client", "message": "Hello, I'm interested..." }
      ]
    }
    
    Response:
    {
      "aiReply": "Great news! As a US citizen, you can apply..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        client_sequence = data.get('clientSequence', '')
        chat_history = data.get('chatHistory', [])
        
        if not client_sequence:
            return jsonify({"error": "clientSequence is required"}), 400
        
        # Generate AI reply
        ai_reply = generate_ai_reply(
            client_sequence,
            chat_history,
            provider=LLM_PROVIDER
        )
        
        return jsonify({
            "aiReply": ai_reply,
            "provider": LLM_PROVIDER
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/improve-ai', methods=['POST'])
def improve_ai():
    """
    Auto-improve the AI prompt by comparing predicted vs actual consultant reply.
    
    Request:
    {
      "clientSequence": "I'm American and currently in Bali. Can I apply from Indonesia?",
      "chatHistory": [...],
      "consultantReply": "Yes, absolutely! You can apply at the Thai Embassy in Jakarta..."
    }
    
    Response:
    {
      "predictedReply": "Great news! As a US citizen, you can apply...",
      "actualReply": "Yes, absolutely! You can apply...",
      "analysis": "Brief analysis of differences",
      "changesMade": ["Change 1", "Change 2"],
      "updatedPrompt": "You are a visa consultant..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        client_sequence = data.get('clientSequence', '')
        chat_history = data.get('chatHistory', [])
        consultant_reply = data.get('consultantReply', '')
        
        if not client_sequence or not consultant_reply:
            return jsonify({
                "error": "clientSequence and consultantReply are required"
            }), 400
        
        # Generate AI prediction
        ai_reply = generate_ai_reply(
            client_sequence,
            chat_history,
            provider=LLM_PROVIDER
        )
        
        # Improve the prompt
        improvement = improve_prompt_with_editor(
            client_sequence,
            chat_history,
            consultant_reply,
            ai_reply,
            provider=LLM_PROVIDER
        )
        
        return jsonify({
            "predictedReply": ai_reply,
            "actualReply": consultant_reply,
            "analysis": improvement.get('analysis', ''),
            "changesMade": improvement.get('changes_made', []),
            "updatedPrompt": improvement.get('prompt', ''),
            "provider": LLM_PROVIDER
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/improve-ai-manually', methods=['POST'])
def improve_ai_manually():
    """
    Manually update the AI prompt with specific instructions.
    
    Request:
    {
      "instructions": "Be more concise. Always mention appointment booking proactively."
    }
    
    Response:
    {
      "updatedPrompt": "You are a visa consultant...",
      "summary": "Made the following changes: ..."
    }
    """
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        instructions = data.get('instructions', '')
        
        if not instructions:
            return jsonify({"error": "instructions are required"}), 400
        
        # Improve the prompt manually
        result = manually_improve_prompt(instructions, provider=LLM_PROVIDER)
        
        return jsonify({
            "updatedPrompt": result.get('prompt', ''),
            "summary": result.get('summary', ''),
            "provider": LLM_PROVIDER
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/prompt', methods=['GET'])
def get_current_prompt():
    """Get the current chatbot prompt"""
    try:
        prompt = get_prompt('chatbot')
        return jsonify({
            "prompt": prompt,
            "type": "chatbot"
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/prompt-history', methods=['GET'])
def prompt_history():
    """Get prompt change history"""
    try:
        limit = request.args.get('limit', 10, type=int)
        history = get_prompt_history('chatbot', limit=limit)
        return jsonify({
            "history": history,
            "count": len(history)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/train', methods=['POST'])
def train():
    """
    Train AI on sample data
    
    Request:
    {
      "numSamples": 5
    }
    
    Response:
    {
      "results": [...],
      "summary": "Trained on 5 samples"
    }
    """
    try:
        data = request.get_json() or {}
        num_samples = data.get('numSamples', 5)
        
        results = train_on_sample_data(
            num_samples=num_samples,
            provider=LLM_PROVIDER
        )
        
        return jsonify({
            "results": results,
            "summary": f"Trained on {num_samples} samples",
            "provider": LLM_PROVIDER
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
