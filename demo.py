"""
Example: Complete Workflow Demonstration
Shows how to use the AI system end-to-end
"""

from parse_conversations import load_conversations, extract_training_examples
from ai_system import generate_ai_reply, improve_prompt_with_editor
from llm_integration import format_client_sequence, format_consultant_reply
from database import get_prompt, get_prompt_history

def demo_workflow():
    """Demonstrate complete self-learning workflow"""
    
    print("\n" + "="*60)
    print("ISSA COMPASS - SELF-LEARNING AI DEMONSTRATION")
    print("="*60 + "\n")
    
    # Step 1: Load training data
    print("STEP 1: Loading Training Data")
    print("-" * 60)
    conversations = load_conversations()
    examples = extract_training_examples(conversations)
    print(f"✓ Loaded {len(conversations)} conversations")
    print(f"✓ Extracted {len(examples)} training examples\n")
    
    # Step 2: Get a sample conversation
    print("STEP 2: Sample Conversation")
    print("-" * 60)
    example = examples[5]  # Pick an interesting example
    
    client_seq = format_client_sequence(example['client_sequence'])
    chat_hist = example['chat_history']
    real_reply = format_consultant_reply(example['consultant_reply'])
    
    print(f"Client Message:\n  {client_seq[:200]}...\n")
    
    if chat_hist:
        print(f"Previous Messages: {len(chat_hist)}")
        for msg in chat_hist[-2:]:  # Show last 2
            role = "CLIENT" if msg['direction'] == 'in' else "CONSULTANT"
            print(f"  ({role}) {msg['text'][:100]}...")
        print()
    
    # Step 3: Generate AI reply (before training)
    print("STEP 3: Generate AI Reply (Before Training)")
    print("-" * 60)
    print("Calling LLM to generate response...")
    
    try:
        ai_reply = generate_ai_reply(client_seq, chat_hist, provider="groq")
        print(f"\nAI Reply:\n  {ai_reply[:300]}...\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Make sure you have API keys set in .env\n")
        return
    
    print(f"Real Consultant Reply:\n  {real_reply[:300]}...\n")
    
    # Step 4: Compare and improve
    print("STEP 4: Self-Learning - Analyzing Differences")
    print("-" * 60)
    print("Calling Editor LLM to improve the prompt...")
    
    try:
        improvement = improve_prompt_with_editor(
            client_seq,
            chat_hist,
            real_reply,
            ai_reply,
            provider="groq"
        )
        
        print(f"\nAnalysis:\n  {improvement.get('analysis', 'N/A')}\n")
        
        changes = improvement.get('changes_made', [])
        if changes:
            print("Changes Made:")
            for i, change in enumerate(changes, 1):
                print(f"  {i}. {change}")
        print()
        
    except Exception as e:
        print(f"Error during improvement: {e}\n")
        return
    
    # Step 5: Show prompt evolution
    print("STEP 5: Prompt Evolution History")
    print("-" * 60)
    
    try:
        history = get_prompt_history('chatbot', limit=5)
        if history:
            print(f"Found {len(history)} prompt updates:\n")
            for i, record in enumerate(history[:3], 1):
                print(f"{i}. {record.get('change_reason', 'No reason')} ")
                print(f"   Updated: {record.get('created_at', 'Unknown')[:19]}\n")
        else:
            print("No history yet. Train more to see evolution!\n")
    except Exception as e:
        print(f"Could not retrieve history: {e}\n")
    
    # Step 6: Test improved AI
    print("STEP 6: Generate AI Reply (After Training)")
    print("-" * 60)
    print("Generating response with improved prompt...")
    
    try:
        # Use a new example
        new_example = examples[10]
        new_client = format_client_sequence(new_example['client_sequence'])
        new_history = new_example['chat_history']
        
        print(f"\nNew Client Message:\n  {new_client[:200]}...\n")
        
        improved_reply = generate_ai_reply(new_client, new_history, provider="groq")
        print(f"Improved AI Reply:\n  {improved_reply[:300]}...\n")
        
    except Exception as e:
        print(f"Error: {e}\n")
    
    # Summary
    print("="*60)
    print("WORKFLOW COMPLETE!")
    print("="*60)
    print("\nWhat happened:")
    print("1. ✓ Loaded real consultant conversations")
    print("2. ✓ AI generated a response")
    print("3. ✓ Compared AI vs real consultant")
    print("4. ✓ AI improved its own prompt")
    print("5. ✓ Prompt saved to database with version history")
    print("6. ✓ Next reply uses the improved prompt")
    print("\nThis is SELF-LEARNING in action! 🚀")
    print("\nThe AI gets better with every conversation it analyzes.")
    print("="*60 + "\n")


def demo_api_usage():
    """Show how to use the API"""
    
    print("\n" + "="*60)
    print("API USAGE EXAMPLES")
    print("="*60 + "\n")
    
    print("Once you deploy, you can call the API like this:\n")
    
    print("1. Generate Reply:")
    print("""
    curl -X POST https://your-app.railway.app/generate-reply \\
      -H "Content-Type: application/json" \\
      -d '{
        "clientSequence": "I need help with DTV visa",
        "chatHistory": []
      }'
    """)
    
    print("\n2. Auto-Improve:")
    print("""
    curl -X POST https://your-app.railway.app/improve-ai \\
      -H "Content-Type: application/json" \\
      -d '{
        "clientSequence": "What documents?",
        "chatHistory": [],
        "consultantReply": "You need: passport, bank statements, employment letter"
      }'
    """)
    
    print("\n3. Manual Improve:")
    print("""
    curl -X POST https://your-app.railway.app/improve-ai-manually \\
      -H "Content-Type: application/json" \\
      -d '{
        "instructions": "Be more casual and friendly"
      }'
    """)
    
    print("\n" + "="*60 + "\n")


if __name__ == '__main__':
    import sys
    
    print("\nChoose demo:")
    print("1. Complete Workflow (shows self-learning)")
    print("2. API Usage Examples")
    print("3. Both")
    
    choice = input("\nEnter choice (1-3): ").strip()
    
    if choice == '1':
        demo_workflow()
    elif choice == '2':
        demo_api_usage()
    elif choice == '3':
        demo_workflow()
        demo_api_usage()
    else:
        print("Invalid choice. Running workflow demo...")
        demo_workflow()
