from django.shortcuts import render, redirect, get_object_or_404
from django.utils.text import slugify
from django.utils.crypto import get_random_string
from .service import *
from management.models import *

types = Type.objects.all()
groups = Group.objects.all()
category = Category.objects.all()

def post_list(request):
    posts = get_posts()
    return render(request, "page/list.html", {"posts": posts, "types": types, "groups": groups, "category": category})

def post_detail(request, slug):
    post = get_post_by_id(slug)
    if not post:
        return render(request, "404.html", status=404)
    return render(request, "page/detail.html", {"post": post})

def post_create(request):

    if request.method == "POST":
        
        thumbnail_file = request.FILES.get("thumbnail")
        featured_file = request.FILES.get("featured")

        thumbnail_url = None
        featured_url = None
        
        if thumbnail_file:
            thumbnail_url = upload_to_bucket("thumbnails", thumbnail_file)
            
        if featured_file:
            featured_url = upload_to_bucket("featured", featured_file)

        title = request.POST["title"]
        data = {
            "title": title,
            "slug": slugify(title) + "-" + get_random_string(5),
            "unique_id": get_random_string(10),
            "content": request.POST["content"],
            "thumbnail_url": thumbnail_url,
            "featured_image_url": featured_url,
            "groups": request.POST.getlist("groups"),
            "category": request.POST.get("category"),
            "types": request.POST.get("types"),
        }
        create_post(data)
        print(data)
        
        result = create_post(data)
        print("INSERT RESULT:", result)
        
        return redirect("post_list")

    return render(request, "page/create.html", {"types": types, "groups": groups, "category": category})

def post_edit(request, post_id):
    post = get_post_for_update(post_id)
    
    if not post:
        return render(request, "404.html", status=404)

    if request.method == "POST":
        data = {
            "title": request.POST["title"],
            "slug": slugify(request.POST["title"]),
            "content": request.POST["content"],
            "groups": request.POST.getlist("groups"),
            "category": request.POST.get("category"),
            "types": request.POST.get("types"),
        }
        update_post(post_id, data)
        return redirect("post_list")
    
    post_groups = post.get("groups", [])

    return render(request, "page/edit.html", {"post": post, "types": types, "post_groups": post_groups, "groups": groups, "category": category})

def post_delete(request, post_id):
    delete_post(post_id)
    return redirect("post_list")

def to_manage(request):
    return redirect("manage_list")