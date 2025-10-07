# Facebook FAQ Chatbot

**Last Updated:** 6/10/2025  
**Author:** iamchoutun  

This project is a **Facebook Messenger FAQ chatbot** with real-time FAQ editing capabilities. It uses a **FastAPI backend** for webhook and FAQ management and a **Tkinter GUI** (`faq_editor.py`) for live editing of questions and answers. The chatbot can respond to text and image messages and is designed to run on **Render** or locally for development.

------------------------------------------------------------------------------------------------

## Features

- Facebook Messenger integration for automated FAQ responses.
- Rule-based bot using a CSV database for questions and answers.
- Real-time FAQ editing with Tkinter GUI.
- FastAPI backend with webhook support and REST endpoints:
  - `/webhook` – Receive messages from Facebook.
  - `/reload-faq` – Reload FAQs without restarting the server.
  - `/update-faq` – Update FAQs from backend editor.
  - `/faq-data` – Fetch current FAQ data.
- Supports text and image responses.
- Auto-reload FAQs whenever updates are made.
- Deployable on **Render** for continuous uptime.

------------------------------------------------------------------------------------------------

## Installation

1. Clone the repository:
    bash
git clone https://github.com/iamchoutun/chatbot_project.git
cd chatbot_project

2. Create a Python virtual environment (recommended):
python -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows

3. Install dependencies:
pip install -r requirements.txt

4. Copy .env.example to .env and fill in your own values:
PAGE_ACCESS_TOKEN=your_page_access_token_here
VERIFY_TOKEN=your_verify_token_here
BACKEND_HOST=https://your-backend-url.onrender.com

------------------------------------------------------------------------------------------------

## Running
## Backend

Run the FastAPI backend locally or on Render:
python run.py

- The backend exposes endpoints for Facebook Messenger integration and FAQ management.

------------------------------------------------------------------------------------------------

## FAQ Editor

Run the Tkinter GUI to edit FAQs in real-time:
python faq_editor.py

- Fetch FAQs from backend, edit, save locally and push updates to the bot.

------------------------------------------------------------------------------------------------

## Test Chat (Optional)

Test chatbot responses locally:
python test_chat.py

------------------------------------------------------------------------------------------------

## Notes

- Ensure your Facebook page and app are properly set up to receive webhook events.
- FAQ CSV (data/faq.csv) is used as the primary source; changes via GUI or backend editor are auto-applied.
- Supports image responses if answers are formatted as [[IMAGE:<url>]].

------------------------------------------------------------------------------------------------

## License

- This project is licensed under the MIT License.
- This project is intended for internal use in a private organization but remains under MIT License.