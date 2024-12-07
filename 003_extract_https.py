import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

async def fetch_page_with_firefox(url):
    try:
        async with async_playwright() as p:
            # Lancer Firefox
            browser = await p.firefox.launch(headless=True)  # headless=False pour voir le navigateur
            context = await browser.new_context()
            page = await context.new_page()

            print(f"Chargement de la page : {url}")
            # Charger l'URL
            await page.goto(url, wait_until="networkidle")  # Attendre que le réseau soit inactif

            # Extraire le contenu HTML après le chargement
            content = await page.content()
            await browser.close()
            return content
    except Exception as e:
        print(f"Erreur lors de la récupération de la page avec Firefox : {e}")
        return None

def extract_urls_from_html(html):
    try:
        # Parser le contenu avec BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        urls = [loc.text for loc in soup.find_all("loc")]  # Extraire toutes les balises <loc>
        return urls
    except Exception as e:
        print(f"Erreur lors du parsing HTML : {e}")
        return []

if __name__ == "__main__":
    # URL de la page cible
    url = "https://www.leboncoin.fr/auto-ventes_immobilieres-adview-1.xml"

    # Exécuter la récupération et l'extraction
    try:
        html_content = asyncio.run(fetch_page_with_firefox(url))

        if html_content:
            # Extraire les URLs des balises <loc>
            extracted_urls = extract_urls_from_html(html_content)
            print("Données extraites :")
            for extracted_url in extracted_urls:
                print(extracted_url)
        else:
            print("Impossible de récupérer le contenu.")
    except Exception as e:
        print(f"Erreur principale : {e}")
