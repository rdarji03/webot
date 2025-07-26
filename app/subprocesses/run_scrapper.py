
import sys
import os
import io
import asyncio
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import requests
sys.path.append(os.path.abspath(os.path.join(
    os.path.dirname(__file__), '..', '..')))
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from app.services.scrapperStoreService import store_pages
from app.services.scrapperStoreService import store_website

extracted_url = set()


def check_valid_url(website_url):
    try:
        parsed_url = urlparse(website_url)
        if not parsed_url.scheme or not parsed_url.netloc:
            print("Invalid URL format.")
            return False

        response = requests.get(website_url, timeout=10)
        if response.status_code == 200:
            start_extracting_url(response.url, response.text)
            return True
        else:
            print(f"URL returned status code: {response.status_code}")
            return False

    except requests.exceptions.RequestException as e:
        print(f"Error while requesting the URL: {e}")
        return False


def start_extracting_url(base_url, text):
    try:
        soup = BeautifulSoup(text, 'html.parser')
        web_links = soup.find_all('a', href=True)

        for link in web_links:
            full_url = urljoin(base_url, link['href'])
            if full_url not in extracted_url:
                extracted_url.add(full_url)

    except:
        print


def start_extracting_content(link):
    data = {}
    try:
        response = requests.get(link, timeout=10)
        if response.status_code == 200:
            html_content = BeautifulSoup(response.text, 'html.parser')
            for tag in html_content(['footer', 'nav', 'header', 'aside', 'script', 'style', 'form', 'noscript']):
                tag.decompose()
            website_title = html_content.find('title').text
            text = html_content.get_text(separator="\n")
            clean_lines = [line.strip()
                           for line in text.split("\n") if line.strip()]
            website_content = "\n".join(clean_lines)

            data = {
                'link':link,
                'title': website_title,
                'content': website_content,
            }
    except requests.exceptions.RequestException as e:
        print(e)
    return data




async def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <website_url>")
        sys.exit(1)

    website_url = sys.argv[1]
    process = check_valid_url(website_url)
    
    if not process:
        print("Invalid website URL")
        return

    web_data = await store_website(website_url)
    web_id = web_data['data']['id']

    for link in extracted_url:
        scrap = start_extracting_content(link)
        if scrap.get('content'):
            await store_pages(web_id, link,scrap['content'])  # ✅ Now it's correct
        if scrap:
            print(f"\nScraping: {link}")
            print(f"Title: {scrap['title']}")
            print(f"Content:\n{scrap['content']}...")

if __name__ == "__main__":
    asyncio.run(main())  # ✅ Only one asyncio.run() at top-level

