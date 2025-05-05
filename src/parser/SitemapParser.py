import requests
import xml.etree.ElementTree as ET
import json
import csv


class SitemapParser:
    NAMESPACE = "{http://www.sitemaps.org/schemas/sitemap/0.9}"

    def __init__(self, sitemap_url: str, keywords: list):
        self.sitemap_url = sitemap_url
        self.keywords = keywords
        self.urls = set()  # Using a set to avoid duplicates

    def fetch_sitemap(self):
        """Fetch the XML sitemap from the given URL."""
        response = requests.get(self.sitemap_url)
        if response.status_code == 200:
            return response.text
        else:
            raise Exception(f"Failed to fetch sitemap: {response.status_code}")

    def parse_sitemap(self, xml_data):
        """Parse XML and extract product URLs containing the keyword."""
        root = ET.fromstring(xml_data)

        for url in root.findall(f".//{self.NAMESPACE}url"):
            loc = url.find(f"{self.NAMESPACE}loc")
            if loc is not None:
                link = loc.text
                for keyword in self.keywords:
                    if keyword in link:
                        self.urls.add(link)

    def get_filtered_urls(self):
        """Fetch, parse, and return filtered URLs."""
        xml_data = self.fetch_sitemap()
        self.parse_sitemap(xml_data)
        return self.urls

    def save_to_txt(self, filename="dumbbells.txt"):
        """Save results to a plain text file."""
        with open(filename, "w", encoding="utf-8") as f:
            for url in self.urls:
                f.write(url + "\n")
        print(f"Saved {len(self.urls)} URLs to {filename}")

    def save_to_json(self, filename="dumbbells.json"):
        """Save results to a JSON file."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(list(self.urls), f, indent=4)
        print(f"Saved {len(self.urls)} URLs to {filename}")

    def save_to_csv(self, filename="dumbbells.csv"):
        """Save results to a CSV file."""
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["Product URL"])  # Header
            for url in self.urls:
                writer.writerow([url])
        print(f"Saved {len(self.urls)} URLs to {filename}")
