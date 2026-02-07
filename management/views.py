from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponseBadRequest
from .service import *

def manage_list(request):
    mode = request.GET.get("mode", "type")
    title_map = {
        "type": "Types",
        "category": "Categories",
        "group": "Groups",
    }
    title = title_map.get(mode, "Unknown")

    table_map = {
        "type": "types",
        "category": "categories",
        "group": "groups",
    }
    table_name = table_map.get(mode)

    if not table_name:
        data = []
    else:
        try:
            data = fetch_items(table_name)
        except Exception as e:
            data = []
            print(f"Error fetch {table_name}: {e}")

    return render(request, "page/manage_list.html", {
        "data": data,
        "title": title,
        "mode": mode,
    })

def manage_form(request, mode, item_id=None):
    table_map = {
        "type": "types",
        "category": "categories",
        "group": "groups",
    }
    table_name = table_map.get(mode)
    if not table_name:
        return HttpResponseBadRequest("Mode tidak valid~")

    title_map = {
        "type": "Type",
        "category": "Category",
        "group": "Group",
    }
    title = title_map.get(mode, "Item")

    obj = None
    is_edit = item_id is not None

    if is_edit:
        url = f"{settings.SUPABASE_URL}/rest/v1/{table_name}"
        params = {"select": "*", "id": f"eq.{item_id}", "limit": 1}
        response = requests.get(url, headers=HEADERS, params=params)
        try:
            response.raise_for_status()
            items = response.json()
            if items:
                obj = items[0]
            else:
                return render(request, "page/manage_form.html", {
                    "mode": mode, "title": title, "error": f"Item dengan ID {item_id} gak ditemukan di table {table_name} bub~ 😔 Coba cek mode-nya ya!"
                })
        except Exception as e:
            return render(request, "page/manage_form.html", {
                "mode": mode, "title": title, "error": f"Gagal ambil data: {str(e)}"
            })

    if request.method == "POST":
        name = request.POST.get("name")
        if not name:
            return render(request, "page/manage_form.html", {
                "mode": mode, "title": title, "obj": obj, "error": "Nama wajib diisi ya bub~"
            })

        data = {"name": name}

        try:
            if is_edit:
                update_item(table_name, item_id, data)
            else:
                create_item(table_name, data)
            return redirect(f"/management/?mode={mode}")
        except Exception as e:
            return render(request, "page/manage_form.html", {
                "mode": mode, "title": title, "obj": obj, "error": f"Gagal simpan: {str(e)}"
            })

    return render(request, "page/manage_form.html", {
        "mode": mode,
        "title": f"{'Edit' if is_edit else 'Tambah'} {title}",
        "obj": obj,
    })

def manage_delete(request, mode, item_id):
    table_map = {"type": "types", "category": "categories", "group": "groups"}
    table_name = table_map.get(mode)
    if not table_name:
        return HttpResponseBadRequest("Mode tidak valid")

    if request.method == "POST":
        try:
            delete_item(table_name, item_id)
            return redirect(f"/management/?mode={mode}")
        except Exception as e:
            return redirect(f"/management/?mode={mode}&error={str(e)}")

    return redirect(f"/management/?mode={mode}")
    
def to_blog(request):
    return redirect("post_list")