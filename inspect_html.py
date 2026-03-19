import urllib.request

url = "http://fondationscp.wikidot.com/equipement-de-la-branche-francophone"
try:
    with urllib.request.urlopen(url) as response:
        html = response.read().decode('utf-8')
        print(html[:20000]) # Print first 20k chars
except Exception as e:
    print(f"Error: {e}")
