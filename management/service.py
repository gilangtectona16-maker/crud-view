# service.py
import hashlib
import requests
from django.conf import settings

BASE_URL = f"{settings.SUPABASE_URL}/rest/v1/posts"
HEADERS = {
    "apikey": settings.SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
    "Prefer": "return=representation",
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

def login_user(email, password, request):
    url = f"{settings.SUPABASE_URL}/rest/v1/accounts"
    params = {"select": "*", "email": f"eq.{email}", "limit": 1}
    response = requests.get(url, headers=HEADERS, params=params)
    response.raise_for_status()
    users = response.json()
    
    if not users:
        return None
    
    user = users[0]
    input_hash = hashlib.sha256(password.encode()).hexdigest()
    if input_hash != user["password_hash"]:
        return None
    
    # Ambil device & IP dari request
    user_agent = request.META.get('HTTP_USER_AGENT', 'Unknown Device')
    ip = request.META.get('REMOTE_ADDR', 'Unknown IP')
    device_info = f"{user_agent} - {ip}"
    
    # Update user di Supabase: set session aktif
    update_url = f"{settings.SUPABASE_URL}/rest/v1/accounts"
    update_params = {"id": f"eq.{user['id']}"}
    update_data = {
        "last_login_at": "now()",
        "device_info": device_info,
        "ip_address": ip,
        "is_active_session": True
    }
    patch_response = requests.patch(update_url, headers=HEADERS, params=update_params, json=update_data)
    
    return user