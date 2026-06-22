# Inside your LLM initialization script
import os
from dotenv import load_dotenv
from langchain_google_genai.chat_models import ChatGoogleGenerativeAIError
from google.api_core.exceptions import ResourceExhausted, GoogleAPICallError
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

llm = ChatGoogleGenerativeAI(
    model="gemini-2.5-flash",
    temperature=0.3,
    max_retries=6,
    timeout=30,
    google_api_key=os.getenv("GOOGLE_API_KEY")
)
    

def invoke_with_clean_errors(model_instance, prompt_payload):
    try:
        # Run normal request execution
        response = model_instance.invoke(prompt_payload)
        # Return success indicator alongside content
        return {"status": "success", "content": response.content}
        
    except (ResourceExhausted, ChatGoogleGenerativeAIError, GoogleAPICallError) as e:
        # Log the real engineering error to your backend server console behind the scenes
        print(f"Backend Debug Log - Google API Error: {str(e)}")
        
        # Return a safe error dictionary back up to the frontend UI layer
        return {
            "status": "error", 
            "content": "The AI service is temporarily busy or handling too many requests right now. Please wait roughly 12 seconds and try asking your question again."
        }
    except Exception as general_error:
        print(f"Backend Debug Log - Unexpected Error: {str(general_error)}")
        return {
            "status": "error",
            "content": "An unexpected system communication error occurred. Please refresh the page."
        }
