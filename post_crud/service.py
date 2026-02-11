import uuid
import requests
from django.conf import settings

STORAGE_URL = f"{settings.SUPABASE_URL}/storage/v1/object"

HEADERS = {
    "apikey": settings.SUPABASE_SERVICE_KEY,
    "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
    "Content-Type": "application/json",
}

BASE_URL = f"{settings.SUPABASE_URL}/rest/v1/posts"

def upload_to_bucket(bucket_name, file):
    filename = f"{uuid.uuid4()}_{file.name}"

    upload_url = f"{STORAGE_URL}/{bucket_name}/{filename}"

    headers = {
        "apikey": settings.SUPABASE_SERVICE_KEY,
        "Authorization": f"Bearer {settings.SUPABASE_SERVICE_KEY}",
        "Content-Type": file.content_type,
    }

    r = requests.post(
        upload_url,
        headers=headers,
        data=file.read()
    )

    r.raise_for_status()

    public_url = f"{settings.SUPABASE_URL}/storage/v1/object/public/{bucket_name}/{filename}"
    return public_url

def get_posts():
    r = requests.get(
        BASE_URL,
        headers=HEADERS,
        params={
            "select": "*",
            "order": "created_at.desc",
        },
    )
    r.raise_for_status()
    return r.json()


def get_post_for_update(post_id):
    r = requests.get(
        f"{settings.SUPABASE_URL}/rest/v1/posts?id=eq.{post_id}",
        headers=HEADERS
    )
    data = r.json()
    return data[0] if data else None

def get_post_by_id(slug):
    r = requests.get(
        f"{settings.SUPABASE_URL}/rest/v1/posts?slug=eq.{slug}",
        headers=HEADERS
    )
    data = r.json()
    return data[0] if data else None

def create_post(data):
    r = requests.post(
        f"{settings.SUPABASE_URL}/rest/v1/posts",
        headers=HEADERS,
        json=data
    )
    
    print("STATUS:", r.status_code)
    print("RESPONSE:", r.text)

    r.raise_for_status()
    return r.json()

def update_post(post_id, data):
    r = requests.patch(
        f"{settings.SUPABASE_URL}/rest/v1/posts?id=eq.{post_id}",
        headers=HEADERS,
        json=data
    )
    return r.status_code == 204

def delete_post(post_id):
    r = requests.delete(
        f"{settings.SUPABASE_URL}/rest/v1/posts?id=eq.{post_id}",
        headers=HEADERS
    )
    return r.status_code == 204

TYPES_URL = f"{settings.SUPABASE_URL}/rest/v1/types"
GROUPS_URL = f"{settings.SUPABASE_URL}/rest/v1/groups"
CATEGORIES_URL = f"{settings.SUPABASE_URL}/rest/v1/categories"

def fetch_types():
    response = requests.get(TYPES_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()  # list of dicts [{"id": "...", "name": "berita panas"}, ...]

def fetch_groups():
    response = requests.get(GROUPS_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()

def fetch_categories():
    response = requests.get(CATEGORIES_URL, headers=HEADERS)
    response.raise_for_status()
    return response.json()