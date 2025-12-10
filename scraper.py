# scraper.py (Felhő verzió)
import requests
from bs4 import BeautifulSoup
import json
import datetime

# --- BEÁLLÍTÁSOK ---
targets = [
    {
        "name": "Tégla 30 N+F",
        "url": "https://www.obi.hu/falazoelemek/bakonytherm-falazo-blokk-30-nf-30-cm-x-25-cm-x-24-cm/p/3221991", 
        # Itt adjuk meg, hogy milyen típusú elemet keresünk (pl. span)
        "tag": "span",
        # Itt adjuk meg a pontos attribútumot és értékét
        "search_attrs": {"data-ui-name": "ads.price.strong"}
    },
		{
        "name": "Habarcs",
        "url": "https://www.obi.hu/szarazhabarcs/sakret-falazohabarcs-hm-25-kg/p/4105763", 
        # Itt adjuk meg, hogy milyen típusú elemet keresünk (pl. span)
        "tag": "span",
        # Itt adjuk meg a pontos attribútumot és értékét
        "search_attrs": {"data-ui-name": "ads.price.strong"}
    },
		{
        "name": "Tetőléc",
        "url": "https://www.obi.hu/fureszaru/tetolec-lucfenyo-jegenyefenyo-nyers-fureszaru-s10-30-mm-x-50-mm-x-4000-mm/p/4161311", 
        # Itt adjuk meg, hogy milyen típusú elemet keresünk (pl. span)
        "tag": "span",
        # Itt adjuk meg a pontos attribútumot és értékét
        "search_attrs": {"data-ui-name": "ads.price.strong"}
    }
]

print("☁️ Felhő Robot indul...")
database = {}
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for item in targets:
    try:
        response = requests.get(item["url"], headers=headers)
        response.encoding = response.apparent_encoding 
        soup = BeautifulSoup(response.text, 'html.parser')

        price_element = soup.find(item["tag"], attrs=item["search_attrs"])

        if price_element:
            price_text = price_element.get_text()
            clean_price = int(''.join(filter(str.isdigit, price_text)))
            database[item["name"]] = clean_price
            print(f"✅ {item['name']}: {clean_price} Ft")
        else:
            print(f"⚠️ Nincs ár: {item['name']}")
            
    except Exception as e:
        print(f"❌ Hiba: {item['name']} - {e}")

# JSON fájl írása (Helyben, a szerveren)
output = {
    "last_updated": str(datetime.datetime.now()),
    "prices": database
}

with open("friss_arak.json", "w", encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=4)

print("💾 JSON generálva!")