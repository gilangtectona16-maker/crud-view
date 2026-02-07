from django.shortcuts import redirect, render, get_object_or_404
from .models import *

model_map = {
    "type": Type,
    "category": Category,
    "group": Group,
}

# Create your views here.
def manage_list(request):
    mode = request.GET.get("mode", "type")  # default type
    
    model = model_map.get(mode, Type)
    data = model.objects.all()

    title = mode.capitalize()

    return render(request, "page/manage_list.html", {
        "data": data,
        "mode": mode,
        "title": title
    })
    
def manage_create(request):
    mode = request.GET.get("mode", "type")
    model = model_map.get(mode, Type)

    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            error = "Nama tidak boleh kosong"
        elif model.objects.filter(name__iexact=name).exists():
            error = f"{mode.capitalize()} sudah ada"
        else:
            model.objects.create(name=name)
            return redirect(f"/management/?mode={mode}")

    return render(request, "page/manage_form.html", {
        "mode": mode,
        "title": mode.capitalize(),
        "error": error
    })

def manage_edit(request, mode, pk):
    model = model_map.get(mode, Type)
    obj = get_object_or_404(model, id=pk)

    error = None

    if request.method == "POST":
        name = request.POST.get("name", "").strip()

        if not name:
            error = "Nama tidak boleh kosong"
        elif model.objects.filter(name__iexact=name).exclude(id=pk).exists():
            error = f"{mode.capitalize()} sudah ada"
        else:
            obj.name = name
            obj.save()
            return redirect(f"/management/?mode={mode}")

    return render(request, "page/manage_form.html", {
        "mode": mode,
        "title": mode.capitalize(),
        "obj": obj,
        "error": error
    })
    
def manage_delete(request, mode, pk):
    model = model_map.get(mode, Type)
    obj = get_object_or_404(model, id=pk)
    obj.delete()
    return redirect(f"/management/?mode={mode}")
    
def to_blog(request):
    return redirect("post_list")