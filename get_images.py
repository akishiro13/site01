import urllib.request
import re

url = "http://fondationscp.wikidot.com/equipement-de-la-branche-francophone"
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        # Find images in /local--files/
        images = re.findall(r'http://fondationscp.wikidot.com/local--files/equipement-de-la-branche-francophone/[\w\.-]+', html)
        # Also find images that might be relative
        relative_images = re.findall(r'src="/local--files/equipement-de-la-branche-francophone/([\w\.-]+)"', html)
        
        for img in sorted(list(set(images))):
            print(img)
        for img in sorted(list(set(relative_images))):
            print(f"http://fondationscp.wikidot.com/local--files/equipement-de-la-branche-francophone/{img}")
except Exception as e:
    print(f"Error: {e}")
