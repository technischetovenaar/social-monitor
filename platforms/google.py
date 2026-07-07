import requests
import re

def scrape_google(query):
    """
    Scrapt Google Reviews met een brede tekst-regex fallback.
    """
    url = f"https://www.google.com/search?q={query}&hl=nl"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        # Zoek in de ruwe tekst naar patronen zoals "4,8 (150 beoordelingen)" of "4.8 150 Google reviews"
        text = response.text
        match = re.search(r'([3-5][,\.]\d)\s*★*\s*\(?(\d+)\s*(beoordelingen|reviews)', text, re.IGNORECASE)
        
        if match:
            return {
                "rating": float(match.group(1).replace(',', '.')),
                "review_count": int(match.group(2))
            }
            
        return None
    except Exception:
        return None