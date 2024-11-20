 # Document expliquant le projet
 Voici quelques suggestions SEO pour optimiser le contenu de votre site web d'Alaric Tabariès sur https://www.altab.fr :

Ajout de Mots-Clés Pertinents : Bien que la description soit riche en détails, ajouter des mots-clés pertinents peut améliorer le SEO. Par exemple, des mots-clés comme "science ouverte", "archivage scientifique", "lombricompostage", "compostage maison", "élevage de cloportes", "nature et compostage", ou "pratiques écologiques" pourraient attirer un public plus ciblé.

Optimisation des Balises Meta :

Meta Description : Actuellement, il n'y a pas de description unique. Une balise meta description plus concise, orientée SEO, pourrait être :
"Explorez les recherches en science ouverte d'Alaric Tabariès, doctorant à l’Université de Toulon, et découvrez ses expériences en nature, compostage, lombricompostage, et cuisine."

Structuration du Contenu avec des Balises Hn :

Utiliser des balises de titres (H1, H2, H3) de manière logique pour structurer le contenu, en créant une hiérarchie qui aide les moteurs de recherche à comprendre les sections principales comme « À propos », « Travaux de recherche », et « Nature et compostage ».
Liens Internes Optimisés :

Assurez-vous que les liens internes sont bien reliés aux pages pertinentes, ce qui favorisera une meilleure indexation par les moteurs de recherche.
Améliorer le Texte Alternatif pour les Images :

Ajouter des descriptions de texte alternatif pour chaque image, en incluant des mots-clés pertinents, aidera à améliorer le référencement des images sur les moteurs de recherche.
Contenu Actualisé et Blog :

Publier régulièrement des articles sur des sujets liés à vos recherches ou expériences (par exemple, un article détaillé sur le compostage ou l’élevage de cloportes) pourrait attirer plus de visiteurs récurrents et améliorer le référencement naturel.












import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import tempfile
import base64
import io
from selenium import webdriver
import time
from PIL import Image
import matplotlib.pyplot as plt
from wordcloud import WordCloud
import os

# Fonction pour récupérer toutes les images d'une page web avec Selenium
def extraire_images_selenium(url):
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    driver.get(url)
    time.sleep(3)  # Attendre le chargement complet de la page
    soup = BeautifulSoup(driver.page_source, "html.parser")
    driver.quit()
    images = []
    for img in soup.find_all("img"):
        img_url = img.get("src")
        alt_text = img.get("alt", "Pas de texte alternatif")
        if img_url:
            full_url = urljoin(url, img_url) if not img_url.startswith("data:image") else img_url
            images.append({"URL": full_url, "Texte alternatif": alt_text})
    return images

# Fonction pour télécharger et convertir l'image
def telecharger_et_convertir_image(image_info):
    image_url = image_info["URL"]
    try:
        if image_url.startswith("data:image"):
            header, encoded = image_url.split(",", 1)
            image_bytes = base64.b64decode(encoded)
            image = Image.open(io.BytesIO(image_bytes))
        else:
            response = requests.get(image_url)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))

        image = image.convert("RGB")
        with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as tmp_file:
            image.save(tmp_file, format="PNG")
            return tmp_file.name, image
    except Exception as e:
        return f"Erreur : {e}", None

# Fonction d’analyse SEO basique des images
def analyse_seo_image(image_path, alt_text):
    try:
        image = Image.open(image_path)
        width, height = image.size
        file_size_kb = os.path.getsize(image_path) / 1024
        file_name = os.path.basename(image_path)

        # Critères SEO
        recommendations = []
        
        if alt_text == "Pas de texte alternatif" or len(alt_text) < 5:
            recommendations.append("Ajouter un texte alternatif descriptif.")
        if width > 1200 or height > 1200:
            recommendations.append("Redimensionner l'image pour optimiser la taille (max 1200x1200).")
        if file_size_kb > 100:
            recommendations.append("Réduire la taille du fichier (< 100KB recommandé).")
        if not any(keyword in file_name.lower() for keyword in ["image", "img", "photo"]):
            recommendations.append("Renommer le fichier pour inclure des mots-clés descriptifs.")

        return recommendations or ["Image optimisée pour le SEO."]
    except Exception as e:
        return [f"Erreur d'analyse de l'image : {e}"]

# Fonction pour extraire les données de la page
def extraire_donnees_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        st.error(f"Erreur lors de la requête pour {url} : {e}")
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    titre = soup.title.text if soup.title else "Pas de titre"
    meta_description = soup.find("meta", attrs={"name": "description"})
    meta_description = meta_description["content"] if meta_description else "Pas de description"
    meta_keywords = soup.find("meta", attrs={"name": "keywords"})
    meta_keywords = meta_keywords["content"] if meta_keywords else "Pas de mots-clés"
    contenu = " ".join([p.text for p in soup.find_all("p")])
    images = extraire_images_selenium(url)

    return {
        "titre": titre,
        "meta_description": meta_description,
        "meta_keywords": meta_keywords,
        "contenu": contenu,
        "images": images,
    }

# Fonction pour visualiser les longueurs des éléments SEO avec Matplotlib
def visualiser_longueurs_seo(donnees_page):
    data = {
        "Titre": len(donnees_page["titre"]),
        "Description meta": len(donnees_page["meta_description"]),
        "Mots-clés": len(donnees_page["meta_keywords"])
    }
    fig, ax = plt.subplots()
    ax.bar(data.keys(), data.values(), color=["skyblue", "salmon", "lightgreen"])
    ax.set_ylabel("Nombre de caractères")
    ax.set_title("Longueur des éléments SEO")
    st.pyplot(fig)

# Fonction pour créer un nuage de mots pour les mots-clés
def nuage_de_mots(mots_cles):
    mots = mots_cles.split(", ")
    texte = " ".join(mots)
    wordcloud = WordCloud(width=800, height=400, background_color="white").generate(texte)
    fig, ax = plt.subplots()
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")
    st.pyplot(fig)

# Fonction pour générer des recommandations SEO avec une API locale (Ollama ou autre)
def generer_seo_avec_ollama(donnees_page):
    try:
        model = "llama3.2:1b"  # Le modèle est maintenant explicitement passé ici
        prompt = f"""
        Voici les données SEO d'une page web :
        - Titre : {donnees_page['titre']}
        - Description meta : {donnees_page['meta_description']}
        - Mots-clés : {donnees_page['meta_keywords']}
        - Contenu de la page : {donnees_page['contenu']}
        
        Veuillez fournir des recommandations SEO pour améliorer le contenu, l'utilisation des mots-clés et les éléments de la page.
        """
        
        url = "http://127.0.0.1:5000/v1/completions"  # URL correcte de l'API
        headers = {"Content-Type": "application/json"}
        data = {"model": model, "prompt": prompt}  # Assurez-vous que le modèle est passé ici

        # Envoi de la requête POST pour générer des recommandations SEO
        response = requests.post(url, json=data, headers=headers)

        if response.status_code == 200:
            try:
                recommandations = response.json().get("choices", [{}])[0].get("text", "Aucune recommandation générée.")
                return recommandations
            except Exception as e:
                return f"Erreur dans le traitement de la réponse JSON : {e}"
        else:
            return f"Erreur lors de l'appel à l'API : {response.status_code} - {response.text}"

    except requests.exceptions.RequestException as e:
        return f"Erreur de connexion à l'API : {e}"

# Application Streamlit principale
st.title("🔍 Analyse SEO et Visualisation")
url = st.text_input("Entrez l'URL de la page à analyser", "https://www.exemple.com")

if st.button("Analyser"):
    donnees_page = extraire_donnees_page(url)
    if donnees_page:
        st.markdown("### 📝 Informations de base")
        st.markdown(f"**Titre** : {donnees_page['titre']}")
        st.markdown(f"**Description meta** : {donnees_page['meta_description']}")
        st.markdown(f"**Mots-clés** : {donnees_page['meta_keywords']}")

        # Visualisation des longueurs des champs SEO
        st.markdown("### 📊 Longueur des éléments SEO")
        visualiser_longueurs_seo(donnees_page)

        # Nuage de mots pour les mots-clés
        if donnees_page["meta_keywords"] != "Pas de mots-clés":
            st.markdown("### 🌥️ Nuage de mots des mots-clés")
            nuage_de_mots(donnees_page["meta_keywords"])
        else:
            st.write("Aucun mot-clé trouvé.")

        # Analyse et affichage des images avec recommandations SEO dans des expanders
        st.markdown("### 🖼️ Analyse d'images et recommandations SEO")
        for image_info in donnees_page["images"]:
            image_url = image_info.get("URL", "URL indisponible")
            image_path, image = telecharger_et_convertir_image(image_info)
            recommandations = analyse_seo_image(image_path, image_info["Texte alternatif"])
            
            with st.expander(f"Image : {image_url}") :
                col1, col2 = st.columns([1, 2])
                with col1:
                    if image:
                        st.image(image, width=150)
                    else:
                        st.write("Image non disponible")
                with col2:
                    st.markdown(f"**URL de l'image :** {image_url}")
                    st.markdown(f"**Texte alternatif :** {image_info['Texte alternatif']}")
                    st.markdown("**Recommandations SEO :**")
                    for rec in recommandations:
                        st.markdown(f"- {rec}")

        # Recommandations SEO avec Ollama
        st.markdown("### 🛠️ Recommandations SEO personnalisées")
        recommandations = generer_seo_avec_ollama(donnees_page)
        st.markdown(f"**Recommandations :** {recommandations}")

        # Insights SEO supplémentaires
        st.markdown("---")
        st.markdown("### 📊 Insights SEO supplémentaires")
        st.markdown("**Compatibilité mobile et optimisation de la vitesse**")
        st.write("Pour un rapport de compatibilité mobile et des recommandations de vitesse, utilisez un outil tel que Google PageSpeed Insights.")
