import asyncio
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

def extract_urls_from_html(html):
    try:
        # Parser le contenu avec BeautifulSoup
        soup = BeautifulSoup(html, "html.parser")
        urls = [loc.text for loc in soup.find_all("loc")]  # Extraire toutes les balises <loc>
        return urls
    except Exception as e:
        print(f"Erreur lors du parsing HTML : {e}")
        return []

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

async def main():
    base_url = "https://www.leboncoin.fr/auto-ventes_immobilieres-adview-{}.xml"
    extracted_urls = set()
    
    print("Début du processus de récupération des URLs...")
    for i in range(1, 1000):  # Limite à 1000 pages par sécurité
        url = base_url.format(i)
        html_content = await fetch_page_with_firefox(url)

        if not html_content:
            print(f"Aucune donnée valide pour : {url}. Arrêt du processus.")
            break

        urls = extract_urls_from_html(html_content)
        if urls:
            print(f"{len(urls)} URLs extraites depuis : {url}")
            extracted_urls.update(urls)
        else:
            print(f"Aucune URL trouvée dans : {url}. Arrêt du processus.")
            break

    # Sauvegarder les résultats
    if extracted_urls:
        with open("extracted_urls.txt", "w") as file:
            for extracted_url in sorted(extracted_urls):
                file.write(extracted_url + "\n")
        print(f"Extraction terminée. {len(extracted_urls)} URLs enregistrées dans extracted_urls.txt.")
    else:
        print("Aucune URL n'a été extraite.")

if __name__ == "__main__":
    asyncio.run(main())
