import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

urls = [
    "https://psicologiaymente.com/tags/historia-de-la-psicologia",
    "https://psicologiaymente.com/tags/narcisismo",
    "https://psicologiaymente.com/tags/teoria",
    "https://psicologiaymente.com/tags/depresion",
    "https://psicologiaymente.com/tags/terapia",
    "https://psicologiaymente.com/tags/emocion"
]

titulares = []

for url in urls:
    try:
        r = requests.get(url, timeout=10)
        soup = BeautifulSoup(r.text, "html.parser")

        for a in soup.find_all("a"):
            title = a.get_text(strip=True)
            link = a.get("href")

            if title and link and len(title) > 30:
                if link.startswith("/"):
                    base = "/".join(url.split("/")[:3])
                    link = base + link

                titulares.append((title, link))

    except Exception as e:
        print("Error con", url, e)


# crear RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")

ET.SubElement(channel, "title").text = "Noticias de Psicología"
ET.SubElement(channel, "link").text = "https://github.com/"
ET.SubElement(channel, "description").text = "Feed generado automáticamente"
ET.SubElement(channel, "lastBuildDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

for title, link in titulares[:50]:
    item = ET.SubElement(channel, "item")
    ET.SubElement(item, "title").text = title
    ET.SubElement(item, "link").text = link
    ET.SubElement(item, "guid").text = link

tree = ET.ElementTree(rss)
tree.write("rss.xml", encoding="utf-8", xml_declaration=True)
