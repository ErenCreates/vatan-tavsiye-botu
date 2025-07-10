from keep_alive import keep_alive

keep_alive()
from keep_alive import keep_alive
import requests
from bs4 import BeautifulSoup
import json
import os

# Canlı kalmasını sağla
keep_alive()

# Vatan Bilgisayar Tavsiye Sistem URL'si
URL = "https://www.vatanbilgisayar.com/tavsiye-sistem/"
headers = {"User-Agent": "Mozilla/5.0"}

# Sayfayı al
response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

# Ürün başlıklarını çek
product_tags = soup.find_all("h3", class_="product-list__product-name")
current_products = [tag.get_text(strip=True) for tag in product_tags]

# Daha önceki ürünleri oku (dosya varsa)
if os.path.exists("prev_products.json"):
  with open("prev_products.json", "r", encoding="utf-8") as f:
    previous_products = json.load(f)
else:
  previous_products = []

# Yeni ürünleri bul
new_products = [p for p in current_products if p not in previous_products]

# Yeni ürün varsa bildir
if new_products:
  print("🆕 Yeni ürün(ler) geldi:")
  for p in new_products:
    print("👉", p)
else:
  print("🟢 Yeni ürün yok.")

# Güncel listeyi dosyaya yaz
with open("prev_products.json", "w", encoding="utf-8") as f:
  json.dump(current_products, f, ensure_ascii=False, indent=2)
