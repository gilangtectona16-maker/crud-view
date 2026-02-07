# service.py
import requests
from django.conf import settings

BASE_URL = f"{settings.SUPABASE_URL}/rest/v1/posts"
HEADERS = {
    "apikey": settings.SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
    "Prefer": "return=representation",  # biar return data setelah insert/update
}

def fetch_posts(page=1, limit=15, group_name=None):
    params = {
        "select": "*",
        "order": "created_at.desc",
        "limit": limit,
        "offset": (page - 1) * limit,
    }
    
    if group_name:
        # filter array contains group_name (PostgreSQL style)
        params["groups"] = f"cs.{{{group_name}}}"  # cs = contains (untuk array text[])
    
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def fetch_post(unique_id):
    params = {"select": "*", "unique_id": f"eq.{unique_id}", "limit": 1}
    response = requests.get(BASE_URL, headers=HEADERS, params=params)
    data = response.json()
    return data[0] if data else None