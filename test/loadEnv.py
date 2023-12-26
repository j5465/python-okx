import os
from dotenv import load_dotenv

def load_env():
    # Load environment variables from .env file
    load_dotenv()

    # Get environment variables
    api_key = os.getenv("OPENAI_API_KEY")
    api_secret = os.getenv("OPENAI_API_S")
    pass_phrase = os.getenv("pass_phrase")

    # Check if environment variables are present
    if not api_key or not api_secret or not pass_phrase:
        raise ValueError("Environment variables are missing.")

    # Return environment variables as dictionary
    return {
        "api_key": api_key,
        "api_secret": api_secret,
        "pass_phrase": pass_phrase
    }

def load_env_tuple():
    api_data = load_env()

    return api_data['api_key'], api_data['api_secret'], api_data['pass_phrase']

