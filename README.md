# Reddit Summary & Email Bot 🤖📩

A Python-based automation tool that fetches recent discussions from a specific Subreddit, generates a "playful and funny" summary using **Google Gemini**, and emails the summary (along with the raw post data) to a specified recipient.

## 🚀 Features

* **Reddit Scraping:** Uses the Reddit API (PRAW) to fetch the top 10 newest posts from the last 24 hours.
* **AI-Powered Summarization:** Integrates **Google Gemini (GenAI)** to digest the posts and generate a concise, entertaining summary.
* **Automated Emailing:** Sends the AI summary as an email body and attaches the full raw text of the posts as a `.txt` file.
* **Configurable Model:** Easily switch between Gemini models (currently set to `gemini-3-flash-preview`).
* **Logging:** Keeps track of operations and errors in `reddit_bot.log`.

## 🛠️ Tech Stack

* **Language:** Python 3.x
* **APIs:**
* [PRAW](https://praw.readthedocs.io/en/stable/) (Python Reddit API Wrapper)
* [Google GenAI SDK](https://ai.google.dev/) (Gemini)


* **Utilities:** `smtplib` (Email), `python-dotenv` (Environment variables)

## 📂 Project Structure

```text
reddit-bot/
├── app.py           # Main logic (Fetching, Summarizing, Sending Email)
├── config.py        # Configuration & Environment Variable Management
├── .gitignore       # Files to ignore (secrets, logs, cache)
├── .env             # API Keys and Secrets (Not included in repo)
├── reddit_posts.txt # Temporary storage for fetched posts
└── reddit_bot.log   # Runtime logs

```

## ⚙️ Setup & Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Mew-72/reddit-bot
cd reddit-bot

```

### 2. Install Dependencies

Create a virtual environment (optional but recommended) and install the required packages:

```bash
pip install praw google-genai python-dotenv

```

### 3. Environment Configuration

Create a `.env` file in the root directory. You will need API keys from Reddit and Google, and an App Password for your email.

**`.env` file format:**

```ini
# Reddit API Credentials
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret

# Google Gemini API Key
GOOGLE_API_KEY=your_google_api_key

# Email Credentials
EMAIL_ADDRESS=your_email@gmail.com
EMAIL_APP_PASSWORD=your_email_app_password

```

> **Note:** For Gmail, you must enable 2-Step Verification and generate an "App Password" to allow the script to send emails.

## 🏃‍♂️ Usage

Run the script from the command line by passing the **Subreddit Name** and the **Recipient Email**.

**Syntax:**

```bash
python app.py <subreddit_name> <recipient_email>

```

**Example:**
To get a summary of r/python and send it to yourself:

```bash
python app.py python your_email@example.com

```

## 🧠 Configuration (`config.py`)

You can modify `config.py` to change the AI model or temperature (creativity).

```python
# Available Models in config.py
# MODEL_NAME = "gemini-2.5-flash"
MODEL_NAME = "gemini-3-flash-preview" # Current selection
TEMPERATURE = 0.2

```

## 📜 Logs

The bot automatically logs its activity to `reddit_bot.log`. Check this file if the email isn't sent or if the script crashes.

```text
2025-12-18 10:00:00,000 - INFO - Starting Reddit bot...
2025-12-18 10:00:02,123 - INFO - Fetching posts from r/python...
2025-12-18 10:00:05,456 - INFO - Found 10 posts from the last 24 hours.
2025-12-18 10:00:10,789 - INFO - Email sent successfully.

```

## 👤 Author

**[Mew-72](https://github.com/Mew-72/)**