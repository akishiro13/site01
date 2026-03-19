import json
from bs4 import BeautifulSoup

def process():
    file_path = "Foundation Facilities - SCP Foundation.html"
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            html = f.read()
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    soup = BeautifulSoup(html, "html.parser")
    # Finding content in SCP wiki structure, usually in #page-content
    content = soup.find(id="page-content")
    if not content:
        print("Could not find #page-content")
        return
    
    facilities = []
    
    # Typically, the SCP wiki structures these lists as headers followed by paragraphs or lists
    # Another common way is bold text inside unnumbered lists, or strong tags inside p tags, 
    # or divs with collapsible blocks.
    # Let's just grab all headers and their subsequent text to get an idea of the structure,
    # or we can look for specific keywords like "Site-" or "Area-".
    
    headers = content.find_all(['h1', 'h2', 'h3', 'h4'])
    for header in headers:
        title = header.get_text(strip=True)
        # Get elements until the next header
        desc_parts = []
        sibling = header.find_next_sibling()
        while sibling and sibling.name not in ['h1', 'h2', 'h3', 'h4']:
            desc_parts.append(sibling.get_text(separator=' ', strip=True))
            sibling = sibling.find_next_sibling()
        
        facilities.append({
            "title": title,
            "description": "\n".join(desc_parts[:3]) # Limit to first 3 paragraphs
        })
        
    print(f"Found {len(facilities)} headers.")
    with open("facilities.json", "w", encoding="utf-8") as out:
        json.dump(facilities, out, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    process()
