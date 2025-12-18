import sys
import praw
import os
import time
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging
from config import REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET, GOOGLE_API_KEY, EMAIL_ADDRESS, EMAIL_APP_PASSWORD, MODEL_NAME, TEMPERATURE
from google import genai
from google.genai import types

# 🔹 Configure Logging
logging.basicConfig(
    filename=os.path.join(os.path.dirname(__file__),"reddit_bot.log"),  # Log file
    level=logging.INFO,  # Log level
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def log_info(message):
    """Log an info message."""
    logging.info(message)

def log_error(message):
    """Log an error message."""
    logging.error(message)

# 🔹 Reddit Setup
reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="summarybot/1.0 by Mayank"
)

# 🔹 Google Gemini Setup
client = genai.Client(api_key=GOOGLE_API_KEY)

def get_recent_posts(subreddit_name):
    """Fetch posts from the last 24 hours using Reddit's `created` attribute."""
    log_info(f"Fetching posts from r/{subreddit_name}...")

    subreddit = reddit.subreddit(subreddit_name)
    recent_posts = []
    time_cutoff = time.time() - 86400  # 24-hour window

    for post in subreddit.new(limit=10):  # Fetch 10 newest posts
        if post.created > time_cutoff:
            recent_posts.append({
                "title": post.title,
                "url": post.url,
                "text": post.selftext,
                "id": post.id
            })

    log_info(f"Found {len(recent_posts)} posts from the last 24 hours.")
    return recent_posts

def save_posts_to_file(posts, filename="reddit_posts.txt"):
    """Save posts to a text file."""
    log_info("Saving posts to file...")

    with open(filename, "w", encoding="utf-8") as file:
        for post in posts:
            file.write(f"Title: {post['title']}\n")
            file.write(f"URL: {post['url']}\n")
            file.write(f"Text: {post['text']}\n")
            file.write("=" * 80 + "\n\n")  # Separator

    log_info(f"Posts saved to {filename}.")
    return filename

def generate_summary():
    """Generate a summary using Google Gemini"""
    logging.info("Generating summary using Google Gemini...")
    try:
        with open("reddit_posts.txt", "r", encoding="utf-8") as file:
            text = file.read()
        text = "Summarize these recent Reddit posts into key points in a playful and funny style.\n"+text
        response = client.models.generate_content(
            model=MODEL_NAME,
            config=types.GenerateContentConfig(
                temperature=TEMPERATURE
            ),
            contents=types.Part.from_text(
                text=text
            )
        )
        return response.text
    except Exception as e:
        logging.error(f"Error generating summary: {e}")
        return None


def send_email(subject, body, recipient_email, attachment_path):
    """Send an email with the post file attached."""
    sender_email = EMAIL_ADDRESS
    app_password = EMAIL_APP_PASSWORD  # Use App Password if using Gmail

    # Create email
    msg = MIMEMultipart()
    msg["Subject"] = subject
    msg["From"] = sender_email
    msg["To"] = recipient_email

    # Attach the email body
    msg.attach(MIMEText(body, "plain"))

    # Attach the file
    try:
        with open(attachment_path, "rb") as attachment:
            part = MIMEText(attachment.read().decode("utf-8"))
            part.add_header("Content-Disposition", f"attachment; filename={attachment_path}")
            msg.attach(part)

        # Send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, app_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())

        log_info("Email sent successfully.")
    except Exception as e:
        log_error(f"Failed to send email: {e}")

def main():
    subreddit_name = sys.argv[1]

    # Fetch posts
    posts = get_recent_posts(subreddit_name)

    if posts:
        # Save posts to a file
        file_path = save_posts_to_file(posts)

        # Email the file
        email_body = f"Here are the latest posts from r/{subreddit_name}."
        # send_email("Your Daily Reddit Posts", email_body, sys.argv[2], file_path)
        summary = generate_summary()
        if summary:
            # print("Summary Generated:\n", summary)
            send_email("Your Daily Reddit Posts Summary", summary, sys.argv[2], file_path)
    else:
        log_info("No posts found in the last 24 hours. Skipping email.")

# Run the bot
if __name__ == "__main__":
    log_info("Starting Reddit bot...")
    try:
        main()
        log_info("Bot finished successfully.")
    except Exception as e:
        log_error(f"Bot crashed: {e}")
