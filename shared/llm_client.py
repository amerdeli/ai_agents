# shared/llm_client.py
import os
from anthropic import Anthropic
from dotenv import load_dotenv

# Loads variables from your .env file into the environment
load_dotenv()

# Single client instance shared across the entire project
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))