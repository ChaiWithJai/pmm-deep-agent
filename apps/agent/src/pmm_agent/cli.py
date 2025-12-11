"""
PMM Deep Agent CLI

Interactive command-line interface for evaluating and creating PMM assets.
"""

import os
import sys

from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def print_welcome():
    """Print welcome message with examples."""
    print("\n" + "=" * 60)
    print("  PMM Deep Agent - Product Marketing Evaluator")
    print("=" * 60)
    print()
    print("Evaluate positioning, messaging, and marketing assets")
    print("using proven PMM frameworks (April Dunford, Fletch PMM).")
    print()
    print("-" * 60)
    print("Quick picks (type the number):")
    print()
    print("  1. Analyze a homepage URL")
    print("  2. Run a 5-second test")
    print("  3. Detect anti-patterns")
    print("  4. Create positioning canvas")
    print("  5. Build messaging framework")
    print("  6. Compare against competitor")
    print()
    print("-" * 60)
    print("Or just type a question in plain English.")
    print("Type 'help' for examples, 'quit' to exit.")
    print("=" * 60 + "\n")


QUICK_PICKS = {
    "1": "analyze_homepage",
    "2": "five_second_test",
    "3": "anti_patterns",
    "4": "positioning_canvas",
    "5": "messaging_framework",
    "6": "competitor_compare",
}


def handle_quick_pick(pick: str, agent) -> None:
    """Handle quick pick selection."""
    action = QUICK_PICKS.get(pick)

    if action == "analyze_homepage":
        url = input("Enter homepage URL: ").strip()
        if not url:
            print("No URL provided.")
            return
        prompt = f"Run a complete PMM audit on {url}. Include 5-second test, positioning analysis, messaging analysis, and anti-pattern detection."

    elif action == "five_second_test":
        url = input("Enter URL to test: ").strip()
        if not url:
            print("No URL provided.")
            return
        prompt = f"Run a 5-second test on {url}. Tell me: What do they do? Who is it for? What makes them different? What should I do next?"

    elif action == "anti_patterns":
        url = input("Enter URL to scan: ").strip()
        if not url:
            print("No URL provided.")
            return
        prompt = f"Scan {url} for PMM anti-patterns. Look for: unclear positioning, jargon, feature dumping, missing social proof, too many CTAs."

    elif action == "positioning_canvas":
        product = input("Describe your product: ").strip()
        if not product:
            print("No product description provided.")
            return
        audience = input("Who is it for? (optional): ").strip()
        competitors = input("Competitors? (optional, comma-separated): ").strip()

        prompt = f"Create a positioning canvas for: {product}"
        if audience:
            prompt += f"\nTarget audience: {audience}"
        if competitors:
            prompt += f"\nCompetitors: {competitors}"

    elif action == "messaging_framework":
        product = input("Describe your product: ").strip()
        if not product:
            print("No product description provided.")
            return
        prompt = f"Create a complete messaging framework for: {product}. Include value proposition, 3 key message pillars, and proof points."

    elif action == "competitor_compare":
        your_url = input("Your homepage URL: ").strip()
        competitor_url = input("Competitor URL: ").strip()
        if not your_url or not competitor_url:
            print("Both URLs are required.")
            return
        prompt = f"Compare my homepage ({your_url}) against this competitor ({competitor_url}). Identify their weaknesses and my differentiation opportunities."

    else:
        print("Unknown action.")
        return

    run_prompt(agent, prompt)


def run_prompt(agent, prompt: str) -> None:
    """Run a prompt through the agent."""
    print("\nAnalyzing...\n")
    try:
        result = agent.invoke({
            "messages": [{"role": "user", "content": prompt}]
        })
        response = result["messages"][-1].content
        print(response)
        print()
    except Exception as e:
        print(f"\nError: {e}\n")


def main():
    """Main CLI entry point."""
    # Check for API key
    if not os.getenv("ANTHROPIC_API_KEY"):
        print("Error: ANTHROPIC_API_KEY not set.")
        print("Create a .env file with your API key or set the environment variable.")
        sys.exit(1)

    # Import agent (after env is loaded)
    from pmm_agent import create_pmm_agent

    print("\nInitializing PMM Deep Agent...")
    agent = create_pmm_agent()
    print("Ready!")

    print_welcome()

    while True:
        try:
            user_input = input("You: ").strip()

            # Handle exit
            if user_input.lower() in ("exit", "quit", "q", "bye"):
                print("\nGoodbye!")
                break

            if not user_input:
                continue

            # Handle help
            if user_input.lower() in ("help", "?", "h"):
                print_welcome()
                continue

            # Handle quick picks
            if user_input in QUICK_PICKS:
                handle_quick_pick(user_input, agent)
                continue

            # Regular prompt
            run_prompt(agent, user_input)

        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            print("Try a different question, or type 'help' for examples.\n")


if __name__ == "__main__":
    main()
