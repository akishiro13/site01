import requests
from bs4 import BeautifulSoup
import json
import re
import time

urls = [
    "https://scp-wiki.wikidot.com/scp-series",
    "https://scp-wiki.wikidot.com/scp-series-2",
    "https://scp-wiki.wikidot.com/scp-series-3",
    "https://scp-wiki.wikidot.com/scp-series-4",
    "https://scp-wiki.wikidot.com/scp-series-5",
    "https://scp-wiki.wikidot.com/scp-series-6",
    "https://scp-wiki.wikidot.com/scp-series-7",
    "https://scp-wiki.wikidot.com/scp-series-8",
    "https://scp-wiki.wikidot.com/scp-series-9",
    "https://scp-wiki.wikidot.com/scp-series-10",
]

scp_list = []

session = requests.Session()

print("Fetching SCPs from WikiDot...")
for url in urls:
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Look for li tags that match SCP pattern
        count = 0
        for li in soup.find_all("li"):
            text = li.text.strip()
            # Match formats like "SCP-001 - Title" or "SCP-3000 - Title"
            match = re.match(r"^(SCP-\d+(?:-[A-Za-z]+)?)\s*-\s*(.+)$", text)
            if match:
                scp_id = match.group(1).upper()
                scp_title = match.group(2)
                
                # Filter out empty or "Access Denied" ones
                if "[ACCESS DENIED]" not in scp_title.upper() and scp_title != "Access Denied":
                    scp_list.append({
                        "id": scp_id,
                        "title": scp_title,
                        "class": "UNKNOWN" # We don't have object classes from these pages directly
                    })
                    count += 1
        
        print(f"Extracted {count} entries from {url}")
        time.sleep(0.5) # Be polite
    except Exception as e:
        print(f"Failed to fetch {url}: {e}")

print(f"Total extracted: {len(scp_list)}")

with open("scp_list.json", "w", encoding="utf-8") as f:
    json.dump(scp_list, f, indent=2)

print("Saved to scp_list.json")
