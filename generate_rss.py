import requests
from bs4 import BeautifulSoup
from datetime import datetime
import xml.etree.ElementTree as ET

# Archivos de entrada/salida en la raíz
links_file = "links.txt"
rss_file = "rss_generated.xml"  # Archivo final generado

# Leer enlaces, ignorando líneas vacías
with open(links_file) as f:
    urls = [line.strip() for line in f if line.strip()]

# Crear estructura básica del RSS
rss = ET.Element("rss", version="2.0")
channel = ET.SubElement(rss, "channel")
ET.SubElement(channel, "title").text = "Mi RSS personalizado"
ET.SubElement(channel, "link").text = "https://github.com/TU_USUARIO/psicorepositorio"
ET.SubElement(channel, "description").text = "RSS generado automáticamente de links.txt"

# Procesar cada URL
for url in urls:
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        soup = BeautifulSoup(r.text, "html.parser")
        title = soup.title.string.strip() if soup.title else "Sin título"

        item = ET.SubElement(channel, "item")
        ET.SubElement(item, "title").text = title
        ET.SubElement(item, "link").text = url
        ET.SubElement(item, "pubDate").text = datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")

    except Exception as e:
        print(f"[ERROR] {url} -> {e}")

# Guardar RSS
tree = ET.ElementTree(rss)
tree.write(rss_file, encoding="utf-8", xml_declaration=True)
print(f"RSS generado en {rss_file}")
