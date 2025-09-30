import os
from dotenv import load_dotenv
from cerebras.cloud.sdk import Cerebras

load_dotenv()

client = Cerebras(
    api_key=os.getenv("CEREBRAS_API_KEY")
)

def analyze_logs_with_cerebras(logs: str) -> str:
    """
    Analyze logs using Cerebras SDK.
    """
    try:
        stream = client.chat.completions.create(
            model="qwen-3-235b-a22b-instruct-2507",   # model from your account
            messages=[
                {"role": "system", "content": "You are a helpful log analysis assistant."},
                {"role": "user", "content": f"Analyze these logs and summarize issues:\n{logs}"}
            ],
            max_completion_tokens=512,
            temperature=0.3,
            stream=True
        )

        response_text = ""
        for chunk in stream:
            response_text += chunk.choices[0].delta.content or ""
        return response_text.strip()

    except Exception as e:
        return f"Error while analyzing logs: {str(e)}"