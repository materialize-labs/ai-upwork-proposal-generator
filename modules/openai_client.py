import os
import openai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve your OpenAI API Key
openai_api_key = os.getenv("OPENAI_API_KEY")

# Setup the OpenAI client
openai.api_key = openai_api_key