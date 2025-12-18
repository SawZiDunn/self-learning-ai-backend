"""
AI System - Core self-learning functionality
Combines LLM, database, and training to create self-improving AI
"""

import json
from typing import Dict, Any, List, Optional
from parse_conversations import extract_training_examples, load_conversations
from llm_integration import (
    generate_llm_response,
    extract_json_from_response,
    format_chat_history,
    format_client_sequence,
    format_consultant_reply
)
from database import get_prompt, update_prompt


def generate_ai_reply(client_sequence: str, chat_history: List[Dict], provider: str = "groq") -> str:
    """
    Generate AI consultant reply given client messages and chat history
    
    Args:
        client_sequence: Client's message(s) as a string
        chat_history: List of previous messages
        provider: LLM provider to use
    
    Returns:
        AI-generated reply as string
    """
    # Get current chatbot prompt from database
    system_prompt = get_prompt('chatbot')
    
    # Format the prompt with current context
    formatted_history = format_chat_history(chat_history)
    
    full_prompt = system_prompt.format(
        chat_history=formatted_history,
        client_sequence=client_sequence
    )
    
    # Generate response
    response = generate_llm_response(full_prompt, provider=provider)
    
    # Extract JSON reply
    try:
        json_response = extract_json_from_response(response)
        return json_response.get('reply', response)
    except Exception as e:
        # Fallback if JSON parsing fails
        print(f"Warning: Failed to parse JSON response: {e}")
        return response


def improve_prompt_with_editor(
    client_sequence: str,
    chat_history: List[Dict],
    consultant_reply: str,
    ai_reply: str,
    provider: str = "groq"
) -> Dict[str, Any]:
    """
    Use editor prompt to analyze and improve the chatbot prompt
    
    Args:
        client_sequence: Client's message(s)
        chat_history: Previous conversation
        consultant_reply: Real consultant's response
        ai_reply: AI's predicted response
        provider: LLM provider to use
    
    Returns:
        Dict with analysis, changes, and updated prompt
    """
    # Get current prompts
    current_chatbot_prompt = get_prompt('chatbot')
    editor_prompt = get_prompt('editor')
    
    # Format the editor prompt
    formatted_history = format_chat_history(chat_history)
    
    full_prompt = editor_prompt.format(
        current_prompt=current_chatbot_prompt,
        client_sequence=client_sequence,
        chat_history=formatted_history,
        consultant_reply=consultant_reply,
        ai_reply=ai_reply
    )
    
    # Generate improvement suggestions
    response = generate_llm_response(full_prompt, provider=provider)
    
    try:
        result = extract_json_from_response(response)
        
        # Update the database with new prompt
        if 'prompt' in result:
            change_reason = f"Auto-improvement: {result.get('analysis', 'No analysis provided')}"
            update_prompt('chatbot', result['prompt'], change_reason)
        
        return result
    except Exception as e:
        print(f"Error parsing editor response: {e}")
        return {
            "analysis": "Failed to parse editor response",
            "changes_made": [],
            "prompt": current_chatbot_prompt
        }


def manually_improve_prompt(instructions: str, provider: str = "groq") -> Dict[str, Any]:
    """
    Manually improve the prompt based on specific instructions
    
    Args:
        instructions: User's instructions for improvement
        provider: LLM provider to use
    
    Returns:
        Dict with updated prompt
    """
    current_prompt = get_prompt('chatbot')
    
    improvement_prompt = f"""You are an AI prompt engineer. Update the following system prompt based on these instructions:

Instructions: {instructions}

Current Prompt:
{current_prompt}

Return the updated prompt in JSON format:
{{"prompt": "updated prompt here", "summary": "brief description of changes made"}}
"""
    
    response = generate_llm_response(improvement_prompt, provider=provider)
    
    try:
        result = extract_json_from_response(response)
        
        if 'prompt' in result:
            change_reason = f"Manual update: {instructions}"
            update_prompt('chatbot', result['prompt'], change_reason)
        
        return result
    except Exception as e:
        print(f"Error: {e}")
        return {"error": str(e), "prompt": current_prompt}


def train_on_sample_data(num_samples: int = 5, provider: str = "groq") -> List[Dict[str, Any]]:
    """
    Train the AI by processing sample conversations and improving the prompt
    
    Args:
        num_samples: Number of training examples to process
        provider: LLM provider to use
    
    Returns:
        List of training results
    """
    print(f"\n{'='*60}")
    print(f"TRAINING AI ON {num_samples} SAMPLES")
    print(f"{'='*60}\n")
    
    # Load training examples
    conversations = load_conversations()
    examples = extract_training_examples(conversations)
    
    # Process samples
    results = []
    for i, example in enumerate(examples[:num_samples]):
        print(f"\n--- Sample {i+1}/{num_samples} ---")
        
        # Prepare data
        client_seq = format_client_sequence(example['client_sequence'])
        chat_hist = example['chat_history']
        real_reply = format_consultant_reply(example['consultant_reply'])
        
        print(f"Client: {client_seq[:100]}...")
        
        # Generate AI reply
        ai_reply = generate_ai_reply(client_seq, chat_hist, provider=provider)
        print(f"AI Reply: {ai_reply[:100]}...")
        print(f"Real Reply: {real_reply[:100]}...")
        
        # Improve prompt
        improvement = improve_prompt_with_editor(
            client_seq,
            chat_hist,
            real_reply,
            ai_reply,
            provider=provider
        )
        
        print(f"Analysis: {improvement.get('analysis', 'No analysis')}")
        
        results.append({
            'sample_num': i + 1,
            'client_sequence': client_seq,
            'ai_reply': ai_reply,
            'real_reply': real_reply,
            'improvement': improvement
        })
    
    print(f"\n{'='*60}")
    print(f"✓ Completed training on {num_samples} samples")
    print(f"{'='*60}\n")
    
    return results


if __name__ == '__main__':
    # Test the system
    print("Testing AI System...")
    
    # Test 1: Generate a reply
    print("\n=== Test 1: Generate AI Reply ===")
    test_client = "I'm interested in the DTV visa. I'm a remote worker from the US."
    test_history = []
    
    try:
        reply = generate_ai_reply(test_client, test_history, provider="groq")
        print(f"Client: {test_client}")
        print(f"AI Reply: {reply}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: Train on sample data
    print("\n=== Test 2: Training ===")
    print("Uncomment the line below to run training:")
    print("# train_on_sample_data(num_samples=3, provider='groq')")
