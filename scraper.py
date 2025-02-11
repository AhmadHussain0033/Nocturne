import os
import time
import json
import random
import requests
import threading
from queue import Queue
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from stem.control import Controller

# Tor Proxy Configuration
TOR_PROXY = "socks5h://127.0.0.1:9050"
TOR_CONTROL_PORT = 9051
TOR_PASSWORD = "your_tor_password"

# Queue for URLs
url_queue = Queue()
visited_urls = set()
scraped_data = []
lock = threading.Lock()

# File Handling
URL_FILE = "urls.txt"

def change_tor_ip():
    """Requests a new Tor identity to change IP address."""
    with Controller.from_port(port=TOR_CONTROL_PORT) as controller:
        controller.authenticate(password=TOR_PASSWORD)
        controller.signal(2)  # NEWNYM signal
        time.sleep(5)  # Wait for new identity

def get_page(url):
    """Fetches a page using Tor."""
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        response = requests.get(url, headers=headers, proxies={"http": TOR_PROXY, "https": TOR_PROXY}, timeout=15)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"[!] Error fetching {url}: {e}")
        return None

def scrape_page(url):
    """Scrapes a page and extracts links."""
    html = get_page(url)
    if not html:
        return None

    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.string if soup.title else "No Title"
    text = " ".join([p.text for p in soup.find_all("p")])
    links = {urljoin(url, a["href"]) for a in soup.find_all("a", href=True)}

    return {"url": url, "title": title, "content": text[:1000], "links": list(links)}

def crawl(depth=1, max_threads=5):
    """Multi-threaded web scraper."""
    def worker():
        while not url_queue.empty():
            url = url_queue.get()
            with lock:
                if url in visited_urls:
                    url_queue.task_done()
                    continue
                visited_urls.add(url)

            print(f"[+] Scraping: {url}")
            data = scrape_page(url)
            if data:
                with lock:
                    scraped_data.append(data)
                    for link in data["links"]:
                        if urlparse(link).netloc.endswith(".onion") and depth > 0:
                            url_queue.put(link)

            url_queue.task_done()
            time.sleep(random.uniform(3, 7))

    threads = []
    for _ in range(max_threads):
        t = threading.Thread(target=worker)
        t.start()
        threads.append(t)

    for t in threads:
        t.join()

def load_urls():
    """Loads .onion URLs from `urls.txt` or creates the file if missing."""
    if not os.path.exists(URL_FILE):
        print(f"[!] `{URL_FILE}` not found. Creating a template file...")
        with open(URL_FILE, "w") as f:
            f.write("http://example1.onion\nhttp://example2.onion\n")  # Sample URLs
        print(f"[✔] Add your `.onion` URLs to `{URL_FILE}` and restart the script.")
        return []

    with open(URL_FILE, "r") as f:
        urls = [line.strip() for line in f if line.strip() and ".onion" in line]
    
    return urls

if __name__ == "__main__":
    # Load URLs from `urls.txt`
    onion_urls = load_urls()
    
    if not onion_urls:
        print("[!] No valid `.onion` URLs found in `urls.txt`. Exiting...")
        exit()

    # Add URLs to Queue
    for url in onion_urls:
        url_queue.put(url)

    # Start Crawling
    crawl_depth = int(input("Enter crawl depth (1-3 recommended): ") or 2)
    num_threads = int(input("Enter number of threads (default 5): ") or 5)
    crawl(depth=crawl_depth, max_threads=num_threads)

    # Save Data
    with open("scraped_data.json", "w", encoding="utf-8") as f:
        json.dump(scraped_data, f, indent=4, ensure_ascii=False)

    print("[✔] Scraping complete! Data saved to `scraped_data.json`")
