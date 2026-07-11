import requests
import re
import json

def scrape_google(place_id_or_query):
    """
    Haalt Google Reviews en de allerlaatste recensie op via Google Maps.
    """
    if place_id_or_query.startswith("ChI"):
        url = f"https://maps.google.com/maps?ftid={place_id_or_query}&hl=nl"
    else:
        url = f"https://www.google.com/search?q={place_id_or_query}&hl=nl"
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "nl-NL,nl;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code != 200:
            return None

        text = response.text
        
        # Algemene statistieken
        match_reviews = re.search(r'(\d+)\s*(beoordelingen|reviews|Google-recensies)', text, re.IGNORECASE)
        match_rating = re.search(r'([3-5][,\.]\d)\s*(★|sterren|out of 5)', text, re.IGNORECASE)
        
        if not match_reviews:
            match_reviews = re.search(r'\(?(\d+)\s*(beoordelingen|reviews)\)?', text, re.IGNORECASE)
        if not match_rating:
            match_rating = re.search(r'([3-5][,\.]\d)', text)

        # Zoek naar specifieke review-teksten in de verborgen JSON-structuur van Google Maps
        # We zoeken naar patronen waarin recensies vaak gecasht staan
        latest_review_text = "Geen tekst achtergelaten"
        latest_review_reviewer = "Anoniem"
        latest_review_rating = None

        # Fallback regex voor een reviewtekst tussen aanhalingstekens in de buurt van sterren
        review_text_match = re.search(r'"([^"]{10,200})"\s*,\s*\[([1-5])\s*,\s*"[^"]+"\]', text)
        if review_text_match:
            latest_review_text = review_text_match.group(1)
            latest_review_rating = float(review_text_match.group(2))
        else:
            # Bredere fallback als de specifieke JSON-match faalt
            fallback_text = re.search(r'“([^”]{5,150})”', text)
            if fallback_text:
                latest_review_text = fallback_text.group(1)

        if match_reviews and match_rating:
            return {
                "rating": float(match_rating.group(1).replace(',', '.')),
                "review_count": int(match_reviews.group(1)),
                "latest_review": {
                    "text": latest_review_text,
                    "reviewer": latest_review_reviewer,
                    "rating": latest_review_rating if latest_review_rating else float(match_rating.group(1).replace(',', '.'))
                }
            }
            
        return None
    except Exception:
        return None