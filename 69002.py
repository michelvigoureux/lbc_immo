import os
import asyncio
from aiofiles import open as aio_open

async def read_urls_from_file(filename="extracted_urls.txt"):
    try:
        async with aio_open(filename, "r") as file:
            urls = [line.strip() for line in await file.readlines()]
        print(f"{len(urls)} URLs lues depuis {filename}")
        return urls
    except Exception as e:
        print(f"Erreur lors de la lecture du fichier {filename} : {e}")
        return []

async def save_urls_to_file(urls, filename="lyon_urls.txt"):
    try:
        async with aio_open(filename, "w") as file:
            await file.writelines(f"{url}\n" for url in urls)
        print(f"{len(urls)} URLs correspondant au critère enregistrées dans {filename}")
    except Exception as e:
        print(f"Erreur lors de l'enregistrement des URLs dans {filename} : {e}")

def download_page_with_curl(url, temp_file="temp_page.html"):
    try:
        command = f"curl -s -A 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)' -o {temp_file} {url}"
        os.system(command)
        return os.path.exists(temp_file)
    except Exception as e:
        print(f"Erreur lors du téléchargement de {url} avec curl : {e}")
        return False

def check_text_in_file(temp_file, text_to_find):
    try:
        with open(temp_file, "r") as file:
            content = file.read()
            return text_to_find in content
    except Exception as e:
        print(f"Erreur lors de la vérification du fichier {temp_file} : {e}")
        return False

def clean_up_temp_file(temp_file):
    try:
        if os.path.exists(temp_file):
            os.remove(temp_file)
            print(f"Fichier temporaire {temp_file} supprimé.")
    except Exception as e:
        print(f"Erreur lors de la suppression du fichier {temp_file} : {e}")

async def process_urls(input_file="extracted_urls.txt", output_file="lyon_urls.txt", text_to_find="69002"):
    urls = await read_urls_from_file(input_file)
    matching_urls = []
    temp_file = "temp_page.html"
    total_count = len(urls)
    processed_count = 0

    for url in urls:
        processed_count += 1
        print(f"Progression : {processed_count}/{total_count} URLs traitées")

        if download_page_with_curl(url, temp_file):
            if check_text_in_file(temp_file, text_to_find):
                matching_urls.append(url)
                print(f"Texte trouvé dans : {url}")
            clean_up_temp_file(temp_file)

    if matching_urls:
        await save_urls_to_file(matching_urls, output_file)
    else:
        print("Aucune URL correspondant au critère n'a été trouvée.")

if __name__ == "__main__":
    asyncio.run(process_urls())
