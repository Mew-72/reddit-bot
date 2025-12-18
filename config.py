import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# 🔹 Reddit API Configuration
REDDIT_CLIENT_ID = os.environ['REDDIT_CLIENT_ID']
REDDIT_CLIENT_SECRET = os.environ['REDDIT_CLIENT_SECRET']

# 🔹 Google API Configuration
# Uncomment and set the model you want to use
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')
# MODEL_NAME = "gemma-3-27b-it"
# MODEL_NAME = "gemma-3-1b-it"
# MODEL_NAME = "gemma-3-12b-it"
# MODEL_NAME = "gemma-3-2b-it"
# MODEL_NAME = "gemma-3-4b-it"
# MODEL_NAME = "gemini-2.5-flash-lite"
# MODEL_NAME = "gemini-2.5-flash"
MODEL_NAME = "gemini-3-flash-preview"
TEMPERATURE = 0.2

# 🔹 Email Configuration
EMAIL_ADDRESS = os.environ['EMAIL_ADDRESS']
EMAIL_APP_PASSWORD = os.environ['EMAIL_APP_PASSWORD']

# Helper Functions
def list_available_models():
    from google import genai
    client = genai.Client(api_key=GOOGLE_API_KEY)
    for model in client.models.list():
        print(model.name)

# Uncomment the line below to list available models when this config is run directly
list_available_models()