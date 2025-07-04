import os
from dotenv import load_dotenv
from agent import HealthWellnessAgent
from context import UserSessionContext
from colorama import init, Fore, Style

def main():
    # Initialize colorama for Windows compatibility
    init()
    
    # Load environment variables
    load_dotenv()
    
    # Initialize context
    context = UserSessionContext(name="User", uid=1, handoff_logs=[], progress_logs=[])
    agent = HealthWellnessAgent(context)
    
    print(f"{Fore.GREEN}Health & Wellness Planner (CLI) 🌟{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type your question or goal (e.g., 'I want to lose 5kg in 2 months').{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type 'history' to view conversation history, 'exit' to quit.{Style.RESET_ALL}")

    while True:
        user_input = input(f"\n{Fore.YELLOW}Your query: {Style.RESET_ALL}").strip()
        
        if user_input.lower() == "exit":
            print(f"{Fore.RED}Goodbye! 👋{Style.RESET_ALL}")
            break
        
        if user_input.lower() == "history":
            if context.progress_logs:
                print(f"\n{Fore.MAGENTA}Conversation History: 📜{Style.RESET_ALL}")
                for i, log in enumerate(context.progress_logs, 1):
                    print(f"{Fore.CYAN}{i}. You: {log['query']}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}   Response: {log['response']}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}No conversation history yet. 📭{Style.RESET_ALL}")
            continue
        
        if not user_input:
            print(f"{Fore.RED}Error: Please enter a valid question or goal. ⚠️{Style.RESET_ALL}")
            continue
        
        response = agent.process_query(user_input)
        print(f"\n{Fore.GREEN}Response: 📋\n{response}{Style.RESET_ALL}")
        context.progress_logs.append({"query": user_input, "response": response})

if __name__ == "__main__":
    main()

