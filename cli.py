import os
from dotenv import load_dotenv
from agent import HealthWellnessAgent
from context import UserSessionContext
from colorama import init, Fore, Style

def get_user_details():
    """Prompt for user details and return them."""
    print(f"{Fore.CYAN}Please enter your details for personalization (press Enter to skip):{Style.RESET_ALL}")
    name = input(f"{Fore.YELLOW}Name (e.g., Sarwat): {Style.RESET_ALL}").strip() or "User"
    age = input(f"{Fore.YELLOW}Age (years, e.g., 25): {Style.RESET_ALL}").strip()
    height = input(f"{Fore.YELLOW}Height (cm, e.g., 165.5): {Style.RESET_ALL}").strip()
    weight = input(f"{Fore.YELLOW}Weight (kg, e.g., 70.0): {Style.RESET_ALL}").strip()
    
    try:
        age = int(age) if age else None
        height = float(height) if height else None
        weight = float(weight) if weight else None
    except ValueError:
        print(f"{Fore.RED}Invalid input for age, height, or weight. Using defaults.{Style.RESET_ALL}")
        age, height, weight = None, None, None
    
    return name, age, height, weight

def main():
    # Initialize colorama for Windows compatibility
    init()
    
    # Load environment variables
    load_dotenv()
    
    # Initialize context
    context = UserSessionContext(name="User", uid=1, age=None, height=None, weight=None, handoff_logs=[], progress_logs=[])
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
                current_type = None
                for i, log in enumerate(context.progress_logs, 1):
                    if log["type"] != current_type:
                        print(f"{Fore.MAGENTA}{log['type'].replace('_', ' ').title()}{Style.RESET_ALL}")
                        current_type = log["type"]
                    print(f"{Fore.CYAN}{i}. You: {log['query']}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}   {log['content']}{Style.RESET_ALL}\n")
            else:
                print(f"{Fore.RED}No conversation history yet. 📭{Style.RESET_ALL}")
            continue
        
        if not user_input:
            print(f"{Fore.RED}Error: Please enter a valid question or goal. ⚠️{Style.RESET_ALL}")
            continue
        
        # Prompt for personalization choice
        print(f"\n{Fore.CYAN}Choose response type:{Style.RESET_ALL}")
        print(f"{Fore.CYAN}1. Personalized Information (requires name, age, height, weight){Style.RESET_ALL}")
        print(f"{Fore.CYAN}2. General Information{Style.RESET_ALL}")
        choice = input(f"{Fore.YELLOW}Enter 1 or 2: {Style.RESET_ALL}").strip()
        
        if choice == "1":
            name, age, height, weight = get_user_details()
            context.update_user_details(name=name, age=age, height=height, weight=weight)
            user_details = f"User: {context.name}, Age: {context.age or 'unknown'}, Height: {context.height or 'unknown'} cm, Weight: {context.weight or 'unknown'} kg. "
            full_query = user_details + user_input
        elif choice == "2":
            full_query = user_input
        else:
            print(f"{Fore.RED}Invalid choice. Using general information.{Style.RESET_ALL}")
            full_query = user_input

        response = agent.process_query(full_query)
        responses = []
        # Categorize string response based on keywords
        user_input_lower = user_input.lower()
        if "goal" in user_input_lower:
            responses.append({"type": "goal_plan", "content": response})
        if "workout" in user_input_lower or "exercise" in user_input_lower:
            responses.append({"type": "workout_plan", "content": response})
        if "meal" in user_input_lower or "diet" in user_input_lower:
            responses.append({"type": "meal_plan", "content": response})
        if "schedule" in user_input_lower or "plan" in user_input_lower:
            responses.append({"type": "schedule", "content": response})
        if "track" in user_input_lower or "progress" in user_input_lower:
            responses.append({"type": "track", "content": response})
        if not responses:
            responses.append({"type": "general", "content": response})

        for resp in responses:
            print(f"\n{Fore.GREEN}{resp['type'].replace('_', ' ').title()}: 📋{Style.RESET_ALL}")
            print(f"{Fore.GREEN}{resp['content']}{Style.RESET_ALL}")
            context.progress_logs.append({"query": user_input, "type": resp["type"], "content": resp["content"]})

if __name__ == "__main__":
    main()