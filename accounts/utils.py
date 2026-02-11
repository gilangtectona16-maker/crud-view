from django.shortcuts import redirect
from django.contrib import messages

def require_login(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_authenticated'):
            messages.warning(request, "Eh belum login nih bub~ Yuk masuk dulu~ 🔑😉")
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper