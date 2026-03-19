import json
from bs4 import BeautifulSoup
import re

with open("original.html", "r", encoding="utf-8") as f:
    html = f.read()

soup = BeautifulSoup(html, "html.parser")

map_div = soup.find(id="wiki-tab-0-0")
if not map_div:
    print("Cannot find map div")
    exit()

mainmap = map_div.find("div", class_="mainmap")

pins = []

def extract_enlarge(container, offset_x=0.0, offset_y=0.0, scale_x=1.0, scale_y=1.0):
    for div in container.find_all("div", class_="enlarge", recursive=False):
        style = div.get("style", "")
        left_match = re.search(r"left:\s*([\d\.]+)%;?", style)
        top_match = re.search(r"top:\s*([\d\.]+)%;?", style)
        name_div = div.find("div", class_="subtitlemap") or div.find("div", class_="numbermap")
        
        img = div.find("img", recursive=False)
        if not img:
            img = div.find("img")
            
        if left_match and top_match and img:
            px = float(left_match.group(1))
            py = float(top_match.group(1))
            
            real_x = offset_x + (px * scale_x) / 100.0
            real_y = offset_y + (py * scale_y) / 100.0
            
            src = img.get("src", "")
            name_match = re.search(r"([^/]+)\.(?:svg|png|jpg|jpeg)$", src, re.I)
            name = name_match.group(1) if name_match else "Unknown"
            if name_div:
                name += " " + name_div.text.strip()
                
            pins.append({"name": name, "x": round(real_x, 4), "y": round(real_y, 4)})

# Extract direct pins
extract_enlarge(mainmap, 0.0, 0.0, 100.0, 100.0)

# Identify mapareas and their following secmaps
elems = list(mainmap.children)
import bs4
for i, el in enumerate(elems):
    if type(el) == bs4.element.Tag and "maparea" in el.get("class", []):
        style = el.get("style", "")
        left_match = re.search(r"left:\s*([\d\.]+)%", style)
        top_match = re.search(r"top:\s*([\d\.]+)%", style)
        width_match = re.search(r"width:\s*([\d\.]+)%", style)
        height_match = re.search(r"height:\s*([\d\.]+)%", style)
        
        if left_match and top_match and width_match and height_match:
            x = float(left_match.group(1))
            y = float(top_match.group(1))
            w = float(width_match.group(1))
            h = float(height_match.group(1))
            
            # Secmap should be the next tag
            for next_el in elems[i+1:]:
                if type(next_el) == bs4.element.Tag and "secmap" in next_el.get("class", []):
                    extract_enlarge(next_el, x, y, w, h)
                    break

with open("map_points.json", "w", encoding="utf-8") as f:
    json.dump(pins, f, indent=2)

print(f"Extracted {len(pins)} points.")
