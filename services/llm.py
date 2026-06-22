import os
from dotenv import load_dotenv
# IMPORT THIS: The exact error types coming out of the integration library
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from google.api_core.exceptions import ResourceExhausted

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_retries=6,
    timeout=30,
    google_api_key=os.getenv(
        "GOOGLE_API_KEY"
    )
)


# Add this safe executor function to run requests
def invoke_with_clean_errors(model_instance, prompt_payload):
    try:
        # Run normal request window execution
        return model_instance.invoke(prompt_payload)
        
    except (ResourceExhausted, ChatGoogleGenerativeAIError):
        # Crucial: Use 'from None' to tell Python to wipe out the huge Google log
        raise Exception("You are out of tokens or requests! Please wait 12 seconds.") from None