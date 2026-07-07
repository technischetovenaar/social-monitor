import requests
from bs4 import BeautifulSoup
import json
import re

def scrape_tiktok(username):
    """
    Haalt TikTok statistieken op door de openbare profielpagina te parseren.
    """
    url = f"https://www.tiktok.com/@{username}"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Runtime-Check": "true"
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        
        if response.status_code != 200:
            print(f"  [TikTok] Pagina gaf status {response.status_code} voor {username}")
            return None
            
        soup = BeautifulSoup(response.text, 'lxml')
        
        # TikTok slaat alle profieldata op in een grote JSON-string in een <script> tag genaamd __UNIVERSAL_DATA_FOR_REHYDRATION__
        script_tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
        
        if script_tag:
            raw_json = json.loads(script_tag.string)
            # Navigeer door de diepe JSON-structuur van TikTok
            default_scope = raw_json.get("__DEFAULT_SCOPE__", {})
            user_detail = default_scope.get("webapp.user-detail", {})
            
            if user_detail and "userInfo" in user_detail:
                stats = user_detail["userInfo"].get("stats", {})
                return {
                    "followers": stats.get("followerCount", 0),
                    "following": stats.get("followingCount", 0),
                    "heart_count": stats.get("heartCount", 0),
                    "video_count": stats.get("videoCount", 0)
                }

        # Alternatieve methode via reguliere expressies als de ID-tag mist
        script_regex = soup.find("script", string=re.compile("followerCount"))
        if script_regex:
            match = re.search(r'"followerCount":(\d+)', script_regex.string)
            if match:
                # Als we alleen volgers kunnen vinden via regex, bouwen we een basis-output
                followers = int(match.group(1))
                return {"followers": followers, "note": "Gevonden via regex-back-up"}

        print(f"  [TikTok] Kon geen statistieken uit de pagina-broncode vissen voor {username}.")
        return None

    except Exception as e:
        print(f"  [TikTok] Fout tijdens het parseren van de pagina: {e}")
        return None