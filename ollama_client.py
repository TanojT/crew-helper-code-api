import requests

OLLAMA_API_URL = "http://localhost:11434/api/generate"

def call_llama(prompt: str, model: str = "llama3.2", stream: bool = False) -> str:
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
        return f"Connection Error: {e}"

def check_ollama_status() -> bool:
    try:
        response = requests.get("http://localhost:11434")
        return response.status_code == 200
    except Exception as e:
        print(f"Ollama connection error: {e}")
        return False
    
def call_llm(prompt: str, model: str = "gpt-4") -> str:
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
    res = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
    return res.json()["choices"][0]["message"]["content"]