import requests
from bs4 import BeautifulSoup
import re

def scrape_instagram(username):
    """
    Haalt Instagram statistieken op via Imginn.
    """
    url = f"https://imginn.com/{username}/"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "nl-NL,nl;q=0.9"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        if response.status_code != 200:
            return None
            
        soup = BeautifulSoup(response.text, 'lxml')
        text_content = soup.get_text()
        
        # We zoeken direct in de platte tekst naar de volgersaantallen
        followers_match = re.search(r'([\d\.,KkMm]+)\s*(followers|volgers)', text_content, re.IGNORECASE)
        posts_match = re.search(r'([\d\.,KkMm]+)\s*(posts|berichten)', text_content, re.IGNORECASE)
        
        stats = {"followers": 0, "posts": 0}
        
        if followers_match:
            raw_num = followers_match.group(1).lower().replace('.', '').replace(',', '')
            stats["followers"] = int(float(raw_num.replace('k', '')) * 1000) if 'k' in raw_num else int(raw_num)
        if posts_match:
            raw_posts = posts_match.group(1).lower().replace('.', '').replace(',', '')
            stats["posts"] = int(raw_posts) if raw_posts.isdigit() else 0
            
        return stats if stats["followers"] > 0 else None

    except Exception:
        return None