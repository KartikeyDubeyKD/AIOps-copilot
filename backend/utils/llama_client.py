import os
from dotenv import load_dotenv
from huggingface_hub import InferenceClient

load_dotenv()

HF_TOKEN = os.getenv("HF_API_TOKEN")
MODEL_NAME = "meta-llama/Llama-3.1-8B-Instruct"

client = InferenceClient(model=MODEL_NAME, token=HF_TOKEN)

def generate_recommendations(log_summary: str) -> str:
    """
    Use Meta LLaMA via Hugging Face Inference API (chat mode).
    """
    messages = [
        {
            "role": "system",
            "content": "You are an experienced SRE assistant. Provide clear, actionable recommendations."
        },
        {
            "role": "user",
            "content": f"Log Summary:\n{log_summary}\n\nPlease suggest 2-3 concrete remediation actions."
        }
    ]

    response = client.chat_completion(
        messages=messages,
        max_tokens=1024,
        temperature=0.5,
        top_p=0.9
    )

    return response.choices[0].message["content"].strip()