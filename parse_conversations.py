"""
CURSOR PROMPT 1 Implementation:
Parse conversations.json to create a list of (client sequence + consultant sequence reply + chat history)
"""

import json
from typing import List, Dict, Any

def load_conversations(filepath: str = 'conversations.json') -> List[Dict[str, Any]]:
    """Load conversations from JSON file"""
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_training_examples(conversations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Extract training examples from conversations.
    Each example contains:
    - client_sequence: List of consecutive client messages
    - consultant_reply: List of consecutive consultant replies
    - chat_history: All previous messages before this client sequence
    """
    training_examples = []
    
    for conversation in conversations:
        messages = conversation.get('conversation', [])
        contact_id = conversation.get('contact_id', 'unknown')
        scenario = conversation.get('scenario', 'unknown')
        
        chat_history = []
        i = 0
        
        while i < len(messages):
            # Collect consecutive client messages (direction "in")
            client_sequence = []
            while i < len(messages) and messages[i]['direction'] == 'in':
                client_sequence.append(messages[i])
                i += 1
            
            # Collect consecutive consultant messages (direction "out")
            consultant_reply = []
            while i < len(messages) and messages[i]['direction'] == 'out':
                consultant_reply.append(messages[i])
                i += 1
            
            # Only add if we have both client and consultant messages
            if client_sequence and consultant_reply:
                example = {
                    'contact_id': contact_id,
                    'scenario': scenario,
                    'client_sequence': client_sequence,
                    'consultant_reply': consultant_reply,
                    'chat_history': chat_history.copy()
                }
                training_examples.append(example)
                
                # Update chat history with this exchange
                chat_history.extend(client_sequence)
                chat_history.extend(consultant_reply)
    
    return training_examples

def format_example_for_display(example: Dict[str, Any]) -> str:
    """Format a training example for readable display"""
    output = []
    output.append(f"{'='*60}")
    output.append(f"Contact ID: {example['contact_id']}")
    output.append(f"Scenario: {example['scenario']}")
    output.append(f"\n--- CHAT HISTORY ({len(example['chat_history'])} messages) ---")
    
    for msg in example['chat_history'][-4:]:  # Show last 4 messages only
        role = "CLIENT" if msg['direction'] == 'in' else "CONSULTANT"
        output.append(f"({role}) {msg['text']}")
    
    if len(example['chat_history']) > 4:
        output.append(f"... ({len(example['chat_history']) - 4} earlier messages)")
    
    output.append(f"\n--- CLIENT SEQUENCE ---")
    for msg in example['client_sequence']:
        output.append(msg['text'])
    
    output.append(f"\n--- CONSULTANT REPLY ---")
    for msg in example['consultant_reply']:
        output.append(msg['text'])
    
    return '\n'.join(output)

def main():
    """Test the conversation parser"""
    print("Loading conversations...")
    conversations = load_conversations()
    print(f"Loaded {len(conversations)} conversations")
    
    print("\nExtracting training examples...")
    training_examples = extract_training_examples(conversations)
    print(f"Extracted {len(training_examples)} training examples")
    
    # Display first 3 examples
    print("\n" + "="*60)
    print("SAMPLE TRAINING EXAMPLES")
    print("="*60)
    
    for i, example in enumerate(training_examples[:3]):
        print(f"\nExample {i+1}:")
        print(format_example_for_display(example))
    
    print(f"\n{'='*60}")
    print(f"Total examples available: {len(training_examples)}")
    
    return training_examples

if __name__ == '__main__':
    examples = main()
