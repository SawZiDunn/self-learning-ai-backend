"""
LLM Integration - supports multiple providers (Groq, Gemini, OpenAI)
"""

import json
import os
from typing import Dict, Any, Optional
from config import Config

# Initialize clients based on available API keys
groq_client = None
gemini_model = None
openai_client = None

if Config.GROQ_API_KEY:
    try:
        from groq import Groq
        groq_client = Groq(api_key=Config.GROQ_API_KEY)
    except ImportError:
        print("Groq package not installed. Run: pip install groq")

if Config.GEMINI_API_KEY:
    try:
        import google.generativeai as genai
        genai.configure(api_key=Config.GEMINI_API_KEY)
        gemini_model = genai.GenerativeModel('gemini-1.5-flash')
    except ImportError:
        print("Gemini package not installed. Run: pip install google-generativeai")

if Config.OPENAI_API_KEY:
    try:
        from openai import OpenAI
        openai_client = OpenAI(api_key=Config.OPENAI_API_KEY)
    except ImportError:
        print("OpenAI package not installed. Run: pip install openai")


def generate_with_groq(prompt: str, model: str = "llama-3.3-70b-versatile") -> str:
    """Generate response using Groq API"""
    if not groq_client:
        raise ValueError("Groq client not initialized. Check GROQ_API_KEY")
    
    response = groq_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content


def generate_with_gemini(prompt: str) -> str:
    """Generate response using Google Gemini API"""
    if not gemini_model:
        raise ValueError("Gemini model not initialized. Check GEMINI_API_KEY")
    
    response = gemini_model.generate_content(prompt)
    return response.text


def generate_with_openai(prompt: str, model: str = "gpt-3.5-turbo") -> str:
    """Generate response using OpenAI API"""
    if not openai_client:
        raise ValueError("OpenAI client not initialized. Check OPENAI_API_KEY")
    
    response = openai_client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=2000
    )
    return response.choices[0].message.content


def generate_llm_response(prompt: str, provider: str = "groq") -> str:
    """
    Generate LLM response using specified provider
    
    Args:
        prompt: The prompt to send to the LLM
        provider: One of "groq", "gemini", "openai"
    
    Returns:
        LLM response as string
    """
    if provider == "groq":
        return generate_with_groq(prompt)
    elif provider == "gemini":
        return generate_with_gemini(prompt)
    elif provider == "openai":
        return generate_with_openai(prompt)
    else:
        raise ValueError(f"Unknown provider: {provider}")


def extract_json_from_response(response: str) -> Dict[str, Any]:
    """
    Extract JSON from LLM response (handles cases where LLM includes extra text)
    """
    # Try to find JSON in the response
    start_idx = response.find('{')
    end_idx = response.rfind('}')
    
    if start_idx == -1 or end_idx == -1:
        raise ValueError(f"No JSON found in response: {response}")
    
    json_str = response[start_idx:end_idx + 1]
    return json.loads(json_str)


def format_chat_history(messages: list) -> str:
    """Format chat history for prompt injection"""
    if not messages:
        return "(No previous messages)"
    
    formatted = []
    for msg in messages:
        role = msg.get('direction', msg.get('role', 'unknown'))
        text = msg.get('text', msg.get('message', ''))
        
        if role in ['in', 'client']:
            formatted.append(f"(CLIENT) {text}")
        elif role in ['out', 'consultant']:
            formatted.append(f"(CONSULTANT) {text}")
    
    return '\n'.join(formatted)


def format_client_sequence(messages: list) -> str:
    """Format client message sequence"""
    if not messages:
        return ""
    
    texts = [msg.get('text', msg.get('message', '')) for msg in messages]
    return '\n'.join(texts)


def format_consultant_reply(messages: list) -> str:
    """Format consultant reply messages"""
    if not messages:
        return ""
    
    texts = [msg.get('text', msg.get('message', '')) for msg in messages]
    return '\n'.join(texts)


# Test function
def test_llm_integration():
    """Test LLM providers"""
    test_prompt = "Say 'Hello! I am working.' in JSON format: {\"message\": \"your message\"}"
    
    print("Testing LLM Integration...")
    print("=" * 60)
    
    if groq_client:
        print("\n✓ Groq API Available")
        try:
            response = generate_with_groq(test_prompt)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\n✗ Groq API Not Available")
    
    if gemini_model:
        print("\n✓ Gemini API Available")
        try:
            response = generate_with_gemini(test_prompt)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\n✗ Gemini API Not Available")
    
    if openai_client:
        print("\n✓ OpenAI API Available")
        try:
            response = generate_with_openai(test_prompt)
            print(f"Response: {response}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        print("\n✗ OpenAI API Not Available")


if __name__ == '__main__':
    test_llm_integration()
