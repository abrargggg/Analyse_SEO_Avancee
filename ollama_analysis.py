import requests
import subprocess

# Function to send request to Ollama API for non-image analysis
def send_request_to_ollama(prompt):
    try:
        # Requête avec le modèle spécifié 'llama3.2:1b'
        response = requests.post(
            "http://127.0.0.1:5000/v1/completions",
            json={
                "model": "llama3.2:1b",  # Gardons ce modèle spécifique
                "prompt": prompt
            }
        )
        response.raise_for_status()  # Vérifier si la requête est réussie
        return response.json().get("choices", [{}])[0].get("text", "No content returned.")
    except requests.exceptions.RequestException as e:
        # Ajout de la réponse complète pour le débogage en cas d'erreur
        if response:
            return f"Error communicating with Ollama: {str(e)}, Response: {response.text}"
        else:
            return f"Error communicating with Ollama: {str(e)}"

# Function for image analysis using moondream
def analyze_image_with_moondream(image_url):
    try:
        result = subprocess.run(
            ["ollama", "run", "moondream", "--image", image_url],
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            return f"Error analyzing image with moondream: {result.stderr}"
        return result.stdout
    except Exception as e:
        return f"Error executing moondream analysis: {str(e)}"
