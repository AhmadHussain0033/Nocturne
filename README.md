# Nocturne

A `.onion` web scraper for the dark web, deep web, and hidden services using Tor, Selenium, and BeautifulSoup.  
This tool automates data extraction, marketplace scraping, API detection, file downloads, and multi-threaded crawling while maintaining anonymity with automatic Tor IP rotation.  

---

## Features  

- Multi-threaded scraping for high-speed crawling  
- Automatic `.onion` discovery using search engines  
- Intelligent link prioritization for important pages  
- Hidden API detection and JSON data extraction  
- Auto-downloads files (`.pdf`, `.txt`, `.csv`, `.zip`)  
- Tor-based anonymity with IP rotation  
- Marketplace scraper for vendors, prices, and ratings  
- Supports `.onion` URLs from `urls.txt`  

---

## Installation  

### Install and Run Tor  

#### Linux (Debian-based)  
```sh
sudo apt update && sudo apt install tor -y
sudo systemctl start tor
```

#### Windows (Tor Browser Required)  
1. Download Tor Browser from [torproject.org](https://www.torproject.org/)  
2. Start Tor Browser  

---

## Usage  

### Add `.onion` Links to `urls.txt`  
Open `urls.txt` and add one URL per line:  

```  
[http://examplemarket.onion](http://examplemarket.onion)  
[http://darkforum.onion](http://darkforum.onion)  
[http://hiddenwiki.onion](http://hiddenwiki.onion)  
```  

### Run the Scraper  
```sh
python scraper.py
```
Then enter:  
```  
Enter crawl depth (1-3 recommended): 2  
Enter number of threads (default 5): 5  
```  

### Search for Hidden `.onion` Sites  
```sh
python scraper.py
```
Then enter:  
```  
Enter mode (search/crawl): search  
Enter search keyword: darknet forums  
```  
This will find `.onion` sites and scrape them.  

---

## Output Files  

| File              | Description                               |
|------------------|----------------------------------|
| `scraped_data.json` | Extracted content, links, and API data. |
| `urls.txt`         | List of `.onion` sites to crawl.        |

---

## Legal Disclaimer  

This tool is for educational and research purposes only.  
The author is not responsible for any misuse of this software.  
Use responsibly and only with permission.  

---

## Contribute  

Fork the repository and open an issue for feature requests or improvements.  

