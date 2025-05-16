import os
import requests
from dotenv import load_dotenv
load_dotenv()

OLLAMA_API_URL = "http://localhost:11434/api/generate"
OPENAI_API_URL = "https://api.openai.com/v1/chat/completions"


headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json"
}

def check_ollama_status() -> bool:
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except Exception as e:
        print(f"Ollama connection error: {e}")
        return False

def call_llm(prompt: str, model: str, stream: bool = False) -> str:
    """
    Routes request to OpenAI or Ollama depending on model name.
    LLaMA models (like llama3.2) go to Ollama.
    GPT models (like gpt-4, gpt-4o) go to OpenAI.
    """
    if model.startswith("llama") or model.startswith("llama3"):
        return call_ollama(prompt, model, stream)
    else:
        return call_openai(prompt, model)

def call_ollama(prompt: str, model: str = "llama3.2", stream: bool = False) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": stream
    }
    try:
        response = requests.post(OLLAMA_API_URL, json=payload)
        if response.status_code == 200:
            return response.json().get("response", "")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"Ollama Connection Error: {e}"

def call_openai(prompt: str, model: str = "gpt-4") -> str:
    headers = {
        "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You are a helpful code assistant."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7
    }
    try:
        response = requests.post(OPENAI_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"OpenAI Connection Error: {e}"