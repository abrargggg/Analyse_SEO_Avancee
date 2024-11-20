import requests

def test_ollama_api():
    url = "http://127.0.0.1:5000/v1/completions"
    payload = {
        "model": "llama3.2:1b",  # Assurez-vous que ce modèle est bien disponible
        "prompt": "Test"
    }
    response = requests.post(url, json=payload)
    
    # Vérifier si la requête a réussi
    if response.status_code == 200:
        print("API Response:", response.json())
    else:
        print(f"Error: {response.status_code} - {response.text}")

test_ollama_api()
