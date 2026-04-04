import asyncio
import aiohttp
import os
from pathlib import Path

async def download_image(session, url, save_path, results): # URL dan rasmni yuklash va saqlash
    try:
        async with session.get(url) as response:
            if response.status == 200:
                content = await response.read()
                filename = os.path.join(save_path, os.path.basename(url))
                with open(filename, 'wb') as f:
                    f.write(content)
                results[url] = "Success"
            else:
                results[url] = "Error"
    except Exception:
        results[url] = "Error"

async def main_async(path, urls, results): # asinxron ravishda barcha URL larni yuklash
    async with aiohttp.ClientSession() as session: # HTTP so'rovlarini yuborish uchun sessiya yaratish
        tasks = [download_image(session, url, str(path), results) for url in urls]
        if tasks:
            await asyncio.gather(*tasks) # barcha yuklash vazifalarini bir vaqtda bajarish

def main():
    while True:
        folder = input("Enter folder path to save images: ").strip()
        if folder == "":
            print("Folder path cannot be empty.")
            continue
        path = Path(folder)
        if not path.exists():
            try:
                path.mkdir(parents=True, exist_ok=True)
            except Exception as e:
                print(f"Cannot create folder: {e}")
                continue
        if not os.access(path, os.W_OK): # W_OK - yozish huquqi borligini tekshirish
            print("No write access to this folder. Enter another path.")
            continue
        break

    # 2. URL larni olish
    urls = []
    results = {}

    print("Enter image URLs (empty line to finish):")
    while True:
        url = input().strip()
        if url == "":
            break
        urls.append(url)

    # 3. Asynchronous yuklash
    loop = asyncio.get_event_loop() # asinxron vazifalarni bajarish uchun event loop yaratish
    loop.run_until_complete(main_async(path, urls, results)) # main_async funksiyasini bajarish va natijalarni kutish

    print("\nSummary of successful and unsuccessful downloads\n")
    print("+----------------------------------------------------------+--------+")
    print("| Link                                                     | Status |")
    print("+----------------------------------------------------------+--------+")
    for url in urls:
        status = results.get(url.rstrip("\\"), "Error")
        print(f"| {url:<58} | {status:<6}|")
    print("+----------------------------------------------------------+--------+")

if __name__ == "__main__":
    main()
