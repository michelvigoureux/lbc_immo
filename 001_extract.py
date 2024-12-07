import asyncio
from pyppeteer import launch

async def fetch_dynamic_page(url):
    # Lancer un navigateur headless
    browser = await launch(headless=True)  # headless=False si vous voulez voir ce qui se passe
    page = await browser.newPage()
    await page.setUserAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")

    # Accéder à la page
    await page.goto(url, {"waitUntil": "networkidle2"})  # Attendre que la page se charge complètement
    content = await page.content()  # Récupérer le contenu HTML généré
    print("Contenu complet de la page :")
    print(content)

    # Fermer le navigateur
    await browser.close()

if __name__ == "__main__":
    url = "https://www.leboncoin.fr/auto-main.xml"
    asyncio.run(fetch_dynamic_page(url))
