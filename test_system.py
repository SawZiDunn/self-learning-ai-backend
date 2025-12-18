"""
Test script to verify all components are working
"""

import sys
from colorama import init, Fore, Style

init(autoreset=True)

def print_test(name, passed):
    """Print test result"""
    if passed:
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {name}")
    else:
        print(f"{Fore.RED}✗{Style.RESET_ALL} {name}")
    return passed

def test_environment():
    """Test environment configuration"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing Environment Configuration{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        from config import Config
        
        has_groq = bool(Config.GROQ_API_KEY)
        has_gemini = bool(Config.GEMINI_API_KEY)
        has_openai = bool(Config.OPENAI_API_KEY)
        has_supabase = bool(Config.SUPABASE_URL and Config.SUPABASE_KEY)
        
        print_test("Config module loaded", True)
        print_test("At least one LLM API key set", has_groq or has_gemini or has_openai)
        
        if has_groq:
            print(f"  {Fore.YELLOW}→{Style.RESET_ALL} Groq API configured")
        if has_gemini:
            print(f"  {Fore.YELLOW}→{Style.RESET_ALL} Gemini API configured")
        if has_openai:
            print(f"  {Fore.YELLOW}→{Style.RESET_ALL} OpenAI API configured")
        
        print_test("Supabase credentials set", has_supabase)
        
        return (has_groq or has_gemini or has_openai) and has_supabase
    except Exception as e:
        print_test("Environment configuration", False)
        print(f"  Error: {e}")
        return False


def test_imports():
    """Test all module imports"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing Module Imports{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    all_passed = True
    
    try:
        import parse_conversations
        print_test("parse_conversations", True)
    except Exception as e:
        print_test("parse_conversations", False)
        print(f"  Error: {e}")
        all_passed = False
    
    try:
        import prompts
        print_test("prompts", True)
    except Exception as e:
        print_test("prompts", False)
        print(f"  Error: {e}")
        all_passed = False
    
    try:
        import llm_integration
        print_test("llm_integration", True)
    except Exception as e:
        print_test("llm_integration", False)
        print(f"  Error: {e}")
        all_passed = False
    
    try:
        import database
        print_test("database", True)
    except Exception as e:
        print_test("database", False)
        print(f"  Error: {e}")
        all_passed = False
    
    try:
        import ai_system
        print_test("ai_system", True)
    except Exception as e:
        print_test("ai_system", False)
        print(f"  Error: {e}")
        all_passed = False
    
    try:
        import app
        print_test("app (Flask)", True)
    except Exception as e:
        print_test("app (Flask)", False)
        print(f"  Error: {e}")
        all_passed = False
    
    return all_passed


def test_conversation_parser():
    """Test conversation parsing"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing Conversation Parser{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        from parse_conversations import load_conversations, extract_training_examples
        
        conversations = load_conversations()
        passed = print_test(f"Load conversations ({len(conversations)} found)", len(conversations) > 0)
        
        if passed:
            examples = extract_training_examples(conversations)
            passed = print_test(f"Extract training examples ({len(examples)} found)", len(examples) > 0)
            
            if passed:
                example = examples[0]
                has_required = all(k in example for k in ['client_sequence', 'consultant_reply', 'chat_history'])
                print_test("Examples have required fields", has_required)
                return has_required
        
        return False
    except Exception as e:
        print_test("Conversation parser", False)
        print(f"  Error: {e}")
        return False


def test_llm_integration():
    """Test LLM integration"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing LLM Integration{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        from llm_integration import groq_client, gemini_model, openai_client
        
        has_groq = print_test("Groq client available", groq_client is not None)
        has_gemini = print_test("Gemini client available", gemini_model is not None)
        has_openai = print_test("OpenAI client available", openai_client is not None)
        
        return has_groq or has_gemini or has_openai
    except Exception as e:
        print_test("LLM integration", False)
        print(f"  Error: {e}")
        return False


def test_database():
    """Test database connection"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Testing Database Connection{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    try:
        from database import supabase, get_prompt
        
        if not supabase:
            print_test("Supabase client initialized", False)
            print(f"  {Fore.YELLOW}Note: Set SUPABASE_URL and SUPABASE_KEY in .env{Style.RESET_ALL}")
            return False
        
        print_test("Supabase client initialized", True)
        
        # Try to get prompt
        try:
            prompt = get_prompt('chatbot')
            print_test("Retrieve prompt from database", len(prompt) > 0)
            return True
        except Exception as e:
            print_test("Retrieve prompt from database", False)
            print(f"  {Fore.YELLOW}Run: python3 -c 'from database import init_database; init_database()'{Style.RESET_ALL}")
            return False
    except Exception as e:
        print_test("Database connection", False)
        print(f"  Error: {e}")
        return False


def run_all_tests():
    """Run all tests"""
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Issa Compass - System Test Suite{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    results = {
        'environment': test_environment(),
        'imports': test_imports(),
        'parser': test_conversation_parser(),
        'llm': test_llm_integration(),
        'database': test_database()
    }
    
    # Summary
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Test Summary{Style.RESET_ALL}")
    print(f"{Fore.CYAN}{'='*60}{Style.RESET_ALL}\n")
    
    passed = sum(results.values())
    total = len(results)
    
    for name, result in results.items():
        status = f"{Fore.GREEN}PASSED{Style.RESET_ALL}" if result else f"{Fore.RED}FAILED{Style.RESET_ALL}"
        print(f"{name.capitalize():20} {status}")
    
    print(f"\n{Fore.CYAN}{'='*60}{Style.RESET_ALL}")
    
    if passed == total:
        print(f"{Fore.GREEN}✓ All tests passed! ({passed}/{total}){Style.RESET_ALL}")
        print(f"\n{Fore.GREEN}Ready to run: python3 app.py{Style.RESET_ALL}")
        return 0
    else:
        print(f"{Fore.YELLOW}⚠ {passed}/{total} tests passed{Style.RESET_ALL}")
        print(f"\n{Fore.YELLOW}Fix the failing tests above before running the app{Style.RESET_ALL}")
        return 1


if __name__ == '__main__':
    try:
        import colorama
    except ImportError:
        print("Installing colorama for better output...")
        import subprocess
        subprocess.check_call([sys.executable, "-m", "pip", "install", "colorama"])
        from colorama import init, Fore, Style
        init(autoreset=True)
    
    sys.exit(run_all_tests())
