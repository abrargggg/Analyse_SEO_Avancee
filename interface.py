import tkinter as tk
from tkinter import scrolledtext
from Analyse_SEO_Avancee.seo_app import fetch_page_data, generate_seo_recommendations

# Fonction pour afficher les résultats d'analyse dans l'interface
def show_results_in_ui(page_data):
    text_area.delete(1.0, tk.END)  # Effacer le contenu de la zone de texte

    # Affichage des informations principales
    text_area.insert(tk.END, f"URL : {page_data['url']}\n")
    text_area.insert(tk.END, f"Titre : {page_data['title']}\n")
    text_area.insert(tk.END, f"Description : {page_data['meta_description']}\n")
    text_area.insert(tk.END, f"Mots-clés : {page_data['meta_keywords']}\n\n")
    
    # Affichage structuré du contenu
    text_area.insert(tk.END, "Contenu (extrait) :\n")
    for i, paragraph in enumerate(page_data.get('content', [])[:5], start=1):
        text_area.insert(tk.END, f"Paragraphe {i}: {paragraph}\n\n")

    # Affichage des images
    if page_data.get('pictures'):
        text_area.insert(tk.END, "Images détectées :\n")
        for i, picture in enumerate(page_data['pictures'], start=1):
            text_area.insert(tk.END, f"Image {i}: {picture}\n")
    else:
        text_area.insert(tk.END, "Aucune image détectée sur la page.\n")
    
    # Affichage des liens internes
    if page_data.get('internal_links'):
        text_area.insert(tk.END, "\nLiens internes détectés :\n")
        for i, link in enumerate(page_data['internal_links'], start=1):
            text_area.insert(tk.END, f"Lien {i}: {link}\n")
    else:
        text_area.insert(tk.END, "Aucun lien interne détecté.\n")
    
    # Affichage des recommandations SEO
    seo_recommendations = generate_seo_recommendations(page_data)
    text_area.insert(tk.END, "\nRecommandations SEO :\n")
    text_area.insert(tk.END, seo_recommendations + "\n")
    text_area.insert(tk.END, "\n" + "-" * 80 + "\n\n")

# Fonction pour analyser une nouvelle URL
def analyze_url():
    url = url_entry.get()
    page_data = fetch_page_data(url)
    if page_data:
        show_results_in_ui(page_data)

# Interface Tkinter
root = tk.Tk()
root.title("Outil d'Analyse de Site Web avec IA")
root.geometry("800x600")

# Champ d'entrée pour l'URL
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=10)
url_entry.insert(0, "https://www.altab.fr")  # URL par défaut

# Zone de texte pour afficher les résultats
text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=90, height=30)
text_area.pack(pady=10)

# Bouton pour lancer l'analyse
analyze_button = tk.Button(root, text="Analyser l'URL", command=analyze_url)
analyze_button.pack(pady=5)

root.mainloop()
