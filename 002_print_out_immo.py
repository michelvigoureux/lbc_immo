import asyncio
from pyppeteer import launch
import re

async def fetch_dynamic_page(url):
    # Lancer un navigateur headless
    browser = await launch(headless=True)
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Accéder à la page
    await page.goto(url, {"waitUntil": "networkidle2"})  # Attendre que la page se charge complètement
    content = await page.content()  # Récupérer le contenu HTML généré

    # Fermer le navigateur
    await browser.close()
    return content

def extract_unique_urls(content):
    # Regex pour extraire les URLs du format souhaité
    pattern = r"https://www\.leboncoin\.fr/auto-ventes_immobilieres-adview-\d+\.xml"
    urls = re.findall(pattern, content)
    # Utiliser un ensemble pour supprimer les doublons
    unique_urls = set(urls)
    return unique_urls

if __name__ == "__main__":
    url = "https://www.leboncoin.fr/auto-main.xml"
    try:
        # Exécuter la récupération de la page
        html_content = asyncio.run(fetch_dynamic_page(url))
        # Extraire les URLs uniques
        unique_urls = extract_unique_urls(html_content)
        # Imprimer les URLs trouvées
        print("URLs uniques extraites :")
        for url in sorted(unique_urls):  # Trier pour un affichage plus lisible
            print(url)
    except Exception as e:
        print(f"Une erreur est survenue : {e}")
