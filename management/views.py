from django.shortcuts import render, redirect
from django.http import Http404
from .service import *

def manage_list(request):
    host = request.get_host()
    parts = host.split('.')
    subdomain = parts[0] if len(parts) > 2 else None

    page = int(request.GET.get("page", 1))
    posts = fetch_posts(page=page, limit=15, group_name=subdomain)

    return render(request, "page/manage_list.html", {
        "posts": posts,
        "active_subdomain": subdomain,
        "page": page,
        # tambahin has_more kalau mau infinite scroll
        "has_more": len(posts) == 15,
    })

def manage_create(request, unique_id, slug):
    post = fetch_post(unique_id)
    if not post:
        raise Http404("Post not found")

    real_slug = post.get("slug")
    if slug != real_slug:
        return redirect("manage_create", unique_id=unique_id, slug=real_slug)

    return render(request, "page/manage_create.html", {"post": post})

def manage_edit(request, group_name):
    page = int(request.GET.get("page", 1))
    limit = 15

    all_group_posts = fetch_posts(page=page, limit=limit*2, group_name=group_name)  # ambil lebih banyak biar bisa split

    # filter di Python kalau types-nya ga di-query langsung
    masonry_posts = [
        p for p in all_group_posts
        if p.get("types") in ["berita panas", "utama"]
    ][:limit]

    carousel_posts = [
        p for p in all_group_posts
        if p.get("types") == "berita panas"
    ][:5]

    context = {
        "group_name": group_name,
        "carousel_posts": carousel_posts,
        "masonry_posts": masonry_posts,
        "page": page,
        "has_more": len(all_group_posts) >= limit,
    }

    return render(request, "page/manage_edit.html", context)

# def manage_delete(request, mode, pk):
#     model = model_map.get(mode, Type)
#     obj = get_object_or_404(model, id=pk)
#     obj.delete()
#     return redirect(f"/management/?mode={mode}")
    
def to_blog(request):
    return redirect("post_list")