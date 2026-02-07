# service.py
import requests
from django.conf import settings

BASE_URL = f"{settings.SUPABASE_URL}/rest/v1/posts"
HEADERS = {
    "apikey": settings.SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
    "Prefer": "return=representation",  # biar return data setelah insert/update
}

def fetch_items(table_name, limit=50):
    url = f"{settings.SUPABASE_URL}/rest/v1/{table_name}"
    params = {
        "select": "*",
        "order": "id.asc",  # atau name.asc kalau ada field name
        "limit": limit,
    }
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return response.json()

def create_item(table_name, data):
    url = f"{settings.SUPABASE_URL}/rest/v1/{table_name}"
    response = requests.post(url, headers=HEADERS, json=data)
    response.raise_for_status()
    return response.json()  # return list inserted data

def update_item(table_name, item_id, data):
    url = f"{settings.SUPABASE_URL}/rest/v1/{table_name}"
    params = {"id": f"eq.{item_id}"}
    response = requests.patch(url, headers=HEADERS, params=params, json=data)
    response.raise_for_status()
    return response.json()

def delete_item(table_name, item_id):
    url = f"{settings.SUPABASE_URL}/rest/v1/{table_name}"
    params = {"id": f"eq.{item_id}"}
    response = requests.delete(url, headers=HEADERS, params=params)
    response.raise_for_status()
    return True  # sukses kalau no error