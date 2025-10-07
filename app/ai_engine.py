import os
import threading
import pandas as pd
from typing import List, Tuple

# Default path to the FAQ CSV file
DATA_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "faq.csv")


class FAQBot:
    """
    Rule-based FAQ bot that retrieves answers from a CSV file.
    
    Features:
    - Thread-safe loading of CSV data.
    - Exact and partial matching for user messages.
    - Automatic reloading of data for up-to-date responses.
    """

    def __init__(self, csv_path: str = DATA_PATH) -> None:
        """
        Initialize the FAQBot with a CSV path and load the FAQ data.
        
        Args:
            csv_path (str): Path to the CSV file containing FAQs.
        """
        self.csv_path = csv_path
        self.lock = threading.Lock()
        self.load_data()

    def load_data(self) -> None:
        """
        Load FAQ data into memory as a list of (question, answer) tuples.
        If the file does not exist, initialize with an empty dataset.
        Thread-safe to allow concurrent usage.
        """
        with self.lock:
            try:
                df = pd.read_csv(self.csv_path, dtype=str).fillna("")
            except FileNotFoundError:
                df = pd.DataFrame(columns=["question", "answer"])
            self.qa_pairs: List[Tuple[str, str]] = [
                (str(row["question"]).strip(), str(row["answer"]).strip())
                for _, row in df.iterrows()
            ]

    def get_answer(self, user_message: str) -> str:
        """
        Retrieve the best-matching answer for a user message.
        Reloads the FAQ data each call to ensure the most recent data is used.
        
        Args:
            user_message (str): The input message from the user.
        
        Returns:
            str: The corresponding answer, or a default response if no match is found.
        """
        self.load_data()
        if not user_message:
            return "Sorry, I did not receive any message."

        msg = user_message.strip().lower()

        # Check for exact match first
        for question, answer in self.qa_pairs:
            if question.lower() == msg:
                return answer

        # Check for partial match
        for question, answer in self.qa_pairs:
            q_lower = question.lower()
            if q_lower and (q_lower in msg or msg in q_lower):
                return answer

        # Default fallback if no match
        return "Sorry, I do not understand your question."

    def reload_faq(self) -> None:
        """
        Manually reload FAQ data from the CSV file.
        """
        self.load_data()


# Global instance for use in other modules
faq_bot = FAQBot()
