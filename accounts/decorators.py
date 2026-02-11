from django.shortcuts import redirect
from django.contrib import messages

def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            messages.warning(request, "Eh kamu belum isi kata kunci nih bub~ Yuk masuk dulu ya~ 🔑😉")
            return redirect('login')  # otomatis ke halaman login
        return view_func(request, *args, **kwargs)
    return wrapper