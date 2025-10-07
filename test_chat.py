"""
Test script for interacting with the FAQBot in console.
Auto-reloads CSV data on every question to ensure latest FAQ is used.
"""

from app.ai_engine import FAQBot

class FAQBotAutoReload(FAQBot):
    """
    Subclass of FAQBot that reloads the FAQ CSV every time
    a question is asked. Useful for testing with frequently
    updated FAQ data.
    """
    def get_answer(self, question: str) -> str:
        self.load_data()  # Reload FAQ data to get the latest updates
        return super().get_answer(question)

def simulate_chat():
    """
    Runs a console-based chat session with the FAQBot.
    User can type 'exit' to quit.
    """
    bot = FAQBotAutoReload()
    print("Chat session started. Type 'exit' to quit.")

    while True:
        user_input = input("You: ").strip()
        if user_input.lower() == "exit":
            print("Chat ended. 👋")
            break

        answer = bot.get_answer(user_input)
        # Detect image responses in the format [[IMAGE:<url>]]
        if isinstance(answer, str) and answer.startswith("[[IMAGE:") and answer.endswith("]]"):
            image_url = answer.replace("[[IMAGE:", "").replace("]]", "").strip()
            print(f"AI: [Image] {image_url}")
        else:
            print(f"AI: {answer}")

if __name__ == "__main__":
    simulate_chat()
