import requests
from bs4 import BeautifulSoup
import json
import csv
import time
import os
from dotenv import load_dotenv
import urllib3

class PrestaShopScraper:
    def __init__(self, urls, limit=3):
        self.urls = urls[:limit]  # Limit the number of URLs to scrape
        self.products = []
        self.session = requests.Session()
        self.login_url = "https://zelart.com.ua/user/login"
        load_dotenv()
        self.email = os.getenv("LOGIN")
        self.password = os.getenv("PASSWORD")
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    def login(self, login_url, email, password):
        """Log in to the website and store the session."""
        headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": login_url,
            "Origin": "https://zelart.com.ua"
        }
        
        # Шаг 1: Получаем страницу логина для извлечения CSRF-токена
        login_page = self.session.get(login_url, headers=headers, verify=False)
        soup = BeautifulSoup(login_page.text, "html.parser")
        
        # Найдите CSRF-токен
        csrf_token = soup.find("input", {"name": "_csrf-frontend"})["value"]
        
        # Шаг 2: Отправляем POST-запрос с CSRF-токеном
        payload = {
            "LoginForm[login]": self.email,  # Поле для email
            "LoginForm[password]": self.password,  # Поле для пароля
            "LoginForm[rememberMe]": "1",  # Запомнить меня (опционально)
            "_csrf-frontend": csrf_token  # CSRF-токен
        }
        try:
            # print("payload", payload)
            response = self.session.post(login_url, data=payload, headers=headers, verify=False)
            if response.status_code == 200 and "logout" in response.text.lower():
                print("Login successful")
            else:
                print("Login failed. Check your credentials or login URL.")
                # print("Response:", response.text)
        except requests.exceptions.RequestException as e:
            print(f"Login error: {e}")
        # print(self.session.cookies.get_dict())

    def fetch_page(self, url):
        """Fetch the HTML content of a product page."""
        headers = {"User-Agent": "Mozilla/5.0"}
        try:
            response = self.session.get(url, headers=headers, verify=False)
            if response.status_code == 200:
                return response.text
            else:
                print(f"Failed to fetch {url} - Status Code: {response.status_code}")
                return None
        except requests.exceptions.SSLError as e:
            print(f"SSL error for {url}: {e}")
            return None

    def parse_product(self, url):
        """Extract title, price, and description from a product page."""
        html = self.fetch_page(url)
        if not html:
            return

        soup = BeautifulSoup(html, "html.parser")

        app_component = soup.find(class_= 'app-component')
        print("app_component:", app_component)

        # Extract title
        title = soup.find("h1")
        title = title.text.strip() if title else "No title found"

        # with open('soup.txt', 'w', encoding='utf-8') as f:
        #     f.write(str(soup))
        # print("soup:", soup)
        # Extract price
        main_price = soup.find(class_="main-price__value")  # Adjust the class name if needed
        main_price = main_price.text.strip() if main_price else "No price found"

        wholesale_amount = soup.find(class_="bonus__desc")  # Adjust the class name if needed
        wholesale_amount = wholesale_amount.text.strip() if wholesale_amount else "No price found"
        
        wholesale_price = soup.find(class_="bonus__sum")  # Adjust the class name if needed
        wholesale_price = wholesale_price.text.strip() if wholesale_price else "No price found"

        recommended_price = soup.find(class_="recommended-price__value")  # Adjust the class name if needed
        recommended_price = recommended_price.text.strip() if recommended_price else "No price found"

        # Extract description
        description = soup.find("div", class_="product-details")  # Adjust class if needed
        description = description.text.strip() if description else "No description found"
    

        # Store product data
        self.products.append(
            {"title": title, 
             "main-price": main_price, 
             "wholesale_amount": wholesale_amount, 
             "wholesale_price": wholesale_price, 
             "recommended_price": recommended_price,
             "description": description, 
             "url": url}
        )
        # print(f"Title: {title}\nMain price: {main_price}\nWholesale amount: {wholesale_amount}\nWholesale price: {wholesale_price}\nRecommended price: {recommended_price}\nDescription: {description}\nURL: {url}\n")

    def scrape_all_products(self):
        """Scrape all product pages."""
        self.login(self.login_url, self.email, self.password)
        for url in self.urls:
            self.parse_product(url)
            time.sleep(1)  # Be polite and avoid getting blocked

    def save_to_json(self, filename="products.json"):
        """Save data to JSON."""
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(self.products, f, indent=4, ensure_ascii=False)
        print(f"Saved {len(self.products)} products to {filename}")

    def save_to_csv(self, filename="products.csv"):
        """Save data to CSV."""
        with open(filename, "w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(
                f, fieldnames=["title", "price", "description", "url"]
            )
            writer.writeheader()
            writer.writerows(self.products)
        print(f"Saved {len(self.products)} products to {filename}")


# Load URLs from a file or list
# with open("dumbbells.txt", "r", encoding="utf-8") as f:
#     product_urls = [line.strip() for line in f.readlines()]

# Run the scraper (limit to 3 products)
