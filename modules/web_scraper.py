import os
import requests
import time
import random
from bs4 import BeautifulSoup
from googlesearch import search

class WebScraper:
    def __init__(self, query=None, num_results=5):
        """Initialize with an optional user query. If None, LUMINA will decide what to scrape."""
        self.query = query
        self.num_results = num_results
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        self.knowledge_base = []

    def decide_query(self):
        """LUMINA determines what to search for based on knowledge gaps."""
        missing_topics = ["Advanced AI models", "Quantum Computing Basics", "Web Development Trends"]  # Example topics
        return random.choice(missing_topics)

    def search_google(self):
        """Use Google to find relevant articles based on the query."""
        if not self.query:
            self.query = self.decide_query()
        
        print(f"Searching Google for: {self.query}")
        search_results = search(self.query, num_results=self.num_results)
        return list(search_results)

    def scrape_page(self, url):
        """Scrape a webpage and extract structured content."""
        try:
            response = requests.get(url, headers=self.headers, timeout=10)
            if response.status_code != 200:
                print(f"Failed to fetch {url}")
                return None
            
            soup = BeautifulSoup(response.text, "html.parser")
            
            title = soup.title.text if soup.title else "No Title"
            headings = [h.text.strip() for h in soup.find_all(["h1", "h2", "h3"])]
            paragraphs = [p.text.strip() for p in soup.find_all("p")]
            code_snippets = [code.text.strip() for code in soup.find_all("code")]
            
            content = {
                "url": url,
                "title": title,
                "headings": headings,
                "paragraphs": paragraphs[:5],  # Store only first 5 paragraphs
                "code_snippets": code_snippets
            }
            return content
        
        except requests.RequestException as e:
            print(f"Error scraping {url}: {e}")
            return None
    
    def scrape_and_store(self):
        """Search, scrape, and store relevant knowledge."""
        urls = self.search_google()
        for url in urls:
            print(f"Scraping: {url}")
            data = self.scrape_page(url)
            if data and self.is_relevant(data):
                self.knowledge_base.append(data)
            time.sleep(random.uniform(2, 5))  # Prevent rate-limiting
        
        print(f"Stored {len(self.knowledge_base)} relevant articles.")
    
    def is_relevant(self, data):
        """Determine if the scraped data is relevant enough to store."""
        return len(data["headings"]) > 0 or len(data["paragraphs"]) > 3
    
    def display_knowledge(self):
        """Display stored knowledge."""
        for item in self.knowledge_base:
            print(f"\nTitle: {item['title']}\nURL: {item['url']}\nHeadings: {', '.join(item['headings'])}\n")

# Example Usage
if __name__ == "__main__":
    user_query = input("Enter a topic to search (or press Enter for LUMINA to decide): ")
    scraper = WebScraper(query=user_query if user_query else None, num_results=3)
    scraper.scrape_and_store()
    scraper.display_knowledge()