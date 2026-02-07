# from pyexpat.errors import messages
# from django.shortcuts import get_object_or_404, redirect, render
# from django.http import HttpResponse
# from .models import Type, Category, Group
# from django.db.models import Q

# # Create your views here.
# def type_list(request):
#     types = Type.objects.all()
#     return render(request, "page/type_list.html", {"types": types})

# def type_create(request):
#     error = None
    
#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()
        
#         if not name:
#             error = "Nama type tidak boleh kosong."
#         # cek unique
#         elif Type.objects.filter(name__iexact=name).exists():
#             error = "Type ini sudah ada."

#         else:
#             Type.objects.create(name=name)
#             return redirect("type_list")

#     return render(request, "page/type_create.html")

# def type_edit(request, type_id):
#     type = get_object_or_404(Type, id=type_id)
#     error = None

#     if request.method == "POST":
#         name = request.POST.get("name", "").strip()

#         if not name:
#             error = "Nama type tidak boleh kosong."

#         elif Type.objects.filter(name__iexact=name).exclude(id=type_id).exists():
#             error = "Type ini sudah ada."

#         else:
#             type.name = name
#             type.save()
#             return redirect("type_list")

#     return render(request, "page/type_edit.html", {"type": type, "error": error})


# def type_delete(request, type_id):
#     type_obj = get_object_or_404(Type, id=type_id)
#     type_obj.delete()
#     return redirect("type_list")

# def to_blog(request):
#     return redirect("post_list")