from flask import Flask
from threading import Thread
import requests
from bs4 import BeautifulSoup
import json
import os
import smtplib
from email.mime.text import MIMEText

# Flask server (canlı tutmak için)
app = Flask('')

@app.route('/')
def home():
    return "Bot çalışıyor!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

keep_alive()

# Mail gönderme fonksiyonu
def send_email(new_products_with_price):
    sender = "namepeira@gmail.com"
    password = "xalvdhkhwmcapuqr"
    receiver = "namepeira@gmail.com"

    body = "🆕 Vatan Bilgisayar'da yeni ürün(ler) eklendi:\n\n"
    for product, price in new_products_with_price:
        body += f"• {product} - Fiyat: {price}\n"

    msg = MIMEText(body)
    msg["Subject"] = "🛒 Yeni Vatan Ürünleri!"
    msg["From"] = sender
    msg["To"] = receiver

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# Web scraping bölümü
URL = "https://www.vatanbilgisayar.com/tavsiye-sistem/"
headers = {"User-Agent": "Mozilla/5.0"}

response = requests.get(URL, headers=headers)
soup = BeautifulSoup(response.content, "html.parser")

products = soup.find_all("div", class_="product-list__item")
current_products_with_price = []

for p in products:
    title_tag = p.find("h3", class_="product-list__product-name")
    price_tag = p.find("div", class_="product-list__price")
    if title_tag and price_tag:
        title = title_tag.get_text(strip=True)
        price = price_tag.get_text(strip=True)
        current_products_with_price.append((title, price))

# Test için öncekileri boş sayıyoruz
previous_products = []


# Sadece ürün isimleri karşılaştırmak için ayır
previous_product_names = [item[0] for item in previous_products]

# Yeni ürünleri bul
new_products = [item for item in current_products_with_price if item[0] not in previous_product_names]

# Yeni ürün varsa hem yazdır, hem mail at
if new_products:
    print("🆕 Yeni ürün(ler) geldi:")
    for p in new_products:
        print("👉", p[0], "-", p[1])
    send_email(new_products)
else:
    print("🟢 Yeni ürün yok.")

# Güncel ürünleri dosyaya kaydet
with open("prev_products.json", "w", encoding="utf-8") as f:
    json.dump(current_products_with_price, f, ensure_ascii=False, indent=2)
