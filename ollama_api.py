import streamlit as st
import requests
import subprocess
from urllib.parse import urljoin

# URL de l'API Ollama pour le modèle Phi3.5
OLLAMA_API_URL = "http://127.0.0.1:5000/v1/completions"

# Fonction pour envoyer une requête à Ollama API pour l'analyse de texte
def send_request_to_ollama(prompt):
    try:
        model = "llama3.2:1b"  # Assurez-vous que le modèle est bien spécifié ici
        # S'assurer que le modèle est transmis correctement dans la requête
        response = requests.post(
            OLLAMA_API_URL,
            json={"model": model, "prompt": prompt}
        )
        response.raise_for_status()  # Vérifier si la requête a échoué
        return response.json().get("choices", [{}])[0].get("text", "No content returned.")
    except requests.exceptions.RequestException as e:
        # Affichage détaillé en cas d'erreur
        if response:
            return f"Error communicating with Ollama: {str(e)}, Response: {response.text}"
        else:
            return f"Error communicating with Ollama: {str(e)}"

# Fonction pour l'analyse d'image avec moondream
def analyze_image_with_moondream(image_url):
    try:
        # Exécuter la commande ollama pour moondream
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

# Analyse des mots-clés et du titre
def analyze_keywords_and_title(page_data):
    prompt = f"""
    SEO analysis of keywords and title:
    URL: {page_data['url']}
    Title: {page_data['title']}
    Description: {page_data.get('meta_description', 'No description')}
    Content excerpt: {''.join(page_data['content'][:200])}
    
    Recommend relevant keywords and optimizations to improve click-through rate (CTR).
    """
    return send_request_to_ollama(prompt)

# Analyse de la structure du contenu
def analyze_content_structure(page_data):
    prompt = f"""
    Content structure analysis for readability improvement:
    URL: {page_data['url']}
    Content excerpt: {''.join(page_data['content'][:500])}
    
    Suggest modifications to enhance readability, section organization, and user engagement.
    """
    return send_request_to_ollama(prompt)

# Fonction modifiée pour analyser les images avec moondream et gérer les URLs relatives
def analyze_image_alts(page_data):
    if not page_data.get("images"):
        return "No images found on the page to analyze alt descriptions."
    
    # Analyse chaque image avec moondream
    alt_analysis_results = []
    for image_url in page_data["images"]:
        # Convertir les URLs relatives en URLs absolues
        full_image_url = urljoin(page_data["url"], image_url)
        alt_analysis_results.append(f"Analysis for {full_image_url}:")
        alt_analysis_results.append(analyze_image_with_moondream(full_image_url))
    
    return "\n".join(alt_analysis_results)

# Analyse des liens internes
def analyze_internal_links(page_data):
    if not page_data.get("internal_links"):
        return "No internal links found on the page."
    
    prompt = f"""
    Internal link analysis for improved site authority and navigation:
    URL: {page_data['url']}
    Internal links: {', '.join(page_data['internal_links'])[:500]}
    
    Recommend enhancements for the internal linking structure to strengthen page authority and user navigation.
    """
    return send_request_to_ollama(prompt)

# Analyse de la description meta et de l'accessibilité mobile
def analyze_meta_description_and_mobile(page_data):
    prompt = f"""
    Analysis of meta description and mobile accessibility:
    URL: {page_data['url']}
    Meta Description: {page_data.get('meta_description', 'No description')}
    
    Suggest improvements for the meta description and check if the page is mobile-friendly.
    """
    return send_request_to_ollama(prompt)

# Interface Streamlit
def main():
    st.title("SEO Analysis Tool")
    
    # Champs d'entrée
    url = st.text_input("Page URL", "https://www.altab.fr")
    title = st.text_input("Title", "Alaric Tabariès")
    meta_description = st.text_area("Meta Description", "Research on open science and archiving practices.")
    content = st.text_area("Content Excerpt", "Explore a world where my passions blend with scientific curiosity...")
    images = st.text_area("Image URLs (comma-separated)", "/images/photo1.jpg, /images/photo2.jpg")
    internal_links = st.text_area("Internal Links (comma-separated)", "/about, /contact, /projects")
    
    page_data = {
        "url": url,
        "title": title,
        "meta_description": meta_description,
        "content": content.split('\n'),  # Convertir le contenu en liste
        "images": images.split(', '),     # Liste des URLs d'images
        "internal_links": internal_links.split(', ')  # Liste des liens internes
    }
    
    # Lancer l'analyse
    if st.button("Analyze"):
        st.subheader("1. Keyword and Title Analysis")
        st.write(analyze_keywords_and_title(page_data))
        
        st.subheader("2. Content Structure Improvement")
        st.write(analyze_content_structure(page_data))
        
        st.subheader("3. Image Alt Descriptions Analysis")
        # Affiche chaque résultat de moondream pour les images
        alt_results = analyze_image_alts(page_data).split("\n")
        for result in alt_results:
            st.write(result)
        
        st.subheader("4. Internal Links Verification")
        st.write(analyze_internal_links(page_data))
        
        st.subheader("5. Meta Description and Mobile Accessibility")
        st.write(analyze_meta_description_and_mobile(page_data))

if __name__ == "__main__":
    main()
