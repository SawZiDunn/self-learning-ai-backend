"""
Supabase Database Integration
Manages AI prompt storage and retrieval
"""

from typing import Optional, Dict, Any
from datetime import datetime
from config import Config

try:
    from supabase import create_client, Client
    supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY) if Config.SUPABASE_URL and Config.SUPABASE_KEY else None
except ImportError:
    print("Supabase package not installed. Run: pip install supabase")
    supabase = None


# Database Schema SQL (for reference - create this in Supabase SQL Editor)
DATABASE_SCHEMA = """
-- Create prompts table
CREATE TABLE IF NOT EXISTS prompts (
    id SERIAL PRIMARY KEY,
    prompt_type VARCHAR(50) NOT NULL,  -- 'chatbot' or 'editor'
    prompt_text TEXT NOT NULL,
    version INTEGER DEFAULT 1,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    metadata JSONB
);

-- Create prompt_history table to track changes
CREATE TABLE IF NOT EXISTS prompt_history (
    id SERIAL PRIMARY KEY,
    prompt_id INTEGER REFERENCES prompts(id),
    old_prompt TEXT,
    new_prompt TEXT,
    change_reason TEXT,
    created_at TIMESTAMP DEFAULT NOW(),
    performance_metrics JSONB
);

-- Create index for faster queries
CREATE INDEX IF NOT EXISTS idx_prompts_type ON prompts(prompt_type);
CREATE INDEX IF NOT EXISTS idx_prompts_updated ON prompts(updated_at DESC);
"""


def init_database():
    """Initialize database with default prompts"""
    if not supabase:
        raise ValueError("Supabase client not initialized")
    
    from prompts import CHATBOT_PROMPT, EDITOR_PROMPT
    
    # Check if chatbot prompt exists
    result = supabase.table('prompts').select('*').eq('prompt_type', 'chatbot').execute()
    
    if not result.data:
        # Insert default chatbot prompt
        supabase.table('prompts').insert({
            'prompt_type': 'chatbot',
            'prompt_text': CHATBOT_PROMPT,
            'version': 1,
            'metadata': {'source': 'initial', 'description': 'Base chatbot prompt'}
        }).execute()
        print("✓ Initialized chatbot prompt in database")
    
    # Check if editor prompt exists
    result = supabase.table('prompts').select('*').eq('prompt_type', 'editor').execute()
    
    if not result.data:
        # Insert default editor prompt
        supabase.table('prompts').insert({
            'prompt_type': 'editor',
            'prompt_text': EDITOR_PROMPT,
            'version': 1,
            'metadata': {'source': 'initial', 'description': 'Prompt editor system'}
        }).execute()
        print("✓ Initialized editor prompt in database")


def get_prompt(prompt_type: str = 'chatbot') -> str:
    """
    Get the latest prompt from database
    
    Args:
        prompt_type: 'chatbot' or 'editor'
    
    Returns:
        The prompt text
    """
    if not supabase:
        # Fallback to local prompts if database unavailable
        from prompts import CHATBOT_PROMPT, EDITOR_PROMPT
        return CHATBOT_PROMPT if prompt_type == 'chatbot' else EDITOR_PROMPT
    
    result = supabase.table('prompts')\
        .select('prompt_text')\
        .eq('prompt_type', prompt_type)\
        .order('updated_at', desc=True)\
        .limit(1)\
        .execute()
    
    if result.data:
        return result.data[0]['prompt_text']
    else:
        raise ValueError(f"No prompt found for type: {prompt_type}")


def update_prompt(prompt_type: str, new_prompt: str, change_reason: str = "Manual update") -> Dict[str, Any]:
    """
    Update prompt in database and log the change
    
    Args:
        prompt_type: 'chatbot' or 'editor'
        new_prompt: The updated prompt text
        change_reason: Explanation of what changed
    
    Returns:
        Updated prompt record
    """
    if not supabase:
        raise ValueError("Supabase client not initialized")
    
    # Get current prompt
    current = supabase.table('prompts')\
        .select('*')\
        .eq('prompt_type', prompt_type)\
        .order('updated_at', desc=True)\
        .limit(1)\
        .execute()
    
    if not current.data:
        raise ValueError(f"No existing prompt found for type: {prompt_type}")
    
    old_prompt = current.data[0]['prompt_text']
    prompt_id = current.data[0]['id']
    old_version = current.data[0]['version']
    
    # Log to history
    supabase.table('prompt_history').insert({
        'prompt_id': prompt_id,
        'old_prompt': old_prompt,
        'new_prompt': new_prompt,
        'change_reason': change_reason
    }).execute()
    
    # Update prompt
    result = supabase.table('prompts')\
        .update({
            'prompt_text': new_prompt,
            'version': old_version + 1,
            'updated_at': datetime.utcnow().isoformat()
        })\
        .eq('id', prompt_id)\
        .execute()
    
    return result.data[0] if result.data else None


def get_prompt_history(prompt_type: str, limit: int = 10) -> list:
    """Get prompt change history"""
    if not supabase:
        return []
    
    # Get prompt ID
    prompt = supabase.table('prompts')\
        .select('id')\
        .eq('prompt_type', prompt_type)\
        .limit(1)\
        .execute()
    
    if not prompt.data:
        return []
    
    prompt_id = prompt.data[0]['id']
    
    # Get history
    result = supabase.table('prompt_history')\
        .select('*')\
        .eq('prompt_id', prompt_id)\
        .order('created_at', desc=True)\
        .limit(limit)\
        .execute()
    
    return result.data


def test_database():
    """Test database connection and operations"""
    print("Testing Supabase Database Integration...")
    print("=" * 60)
    
    if not supabase:
        print("✗ Supabase client not initialized")
        print("Please set SUPABASE_URL and SUPABASE_KEY in .env")
        return
    
    print("✓ Supabase client initialized")
    
    try:
        # Test getting prompt
        prompt = get_prompt('chatbot')
        print(f"✓ Retrieved chatbot prompt ({len(prompt)} characters)")
        
        # Test prompt history
        history = get_prompt_history('chatbot')
        print(f"✓ Retrieved prompt history ({len(history)} records)")
        
        print("\n✅ Database integration working!")
    except Exception as e:
        print(f"\n✗ Error: {e}")


if __name__ == '__main__':
    test_database()
