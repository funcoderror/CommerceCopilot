
from src.tools.tool_calling import run_tool_assistant


def chat():
    print("\n===================================")
    print("       Welcome to CommerceCopilot")
    print("===================================")
    print("Ask me anything about products, orders, or policies.")
    print("Type 'exit', 'quit', or 'bye' to end the conversation.\n")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            continue

        if user_input.lower() in ["exit", "quit", "bye"]:
            print("\nCommerceCopilot: Thank you for shopping with us!")
            break

        try:
            response = run_tool_assistant(user_input)

            print(f"\nCommerceCopilot: {response}\n")

        except Exception as e:
            print(f"\nCommerceCopilot: Sorry, something went wrong: {e}\n")


if __name__ == "__main__":
    chat()
