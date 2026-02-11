from django.shortcuts import render, redirect
from django.contrib import messages
from .hash_utils import check_admin_password
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from .hash_utils import check_admin_password

class CustomTokenObtainPairView(APIView):
    def post(self, request):
        secret_key = request.data.get('secret_key', '').strip()

        if check_admin_password(secret_key):
            refresh = RefreshToken()
            refresh['user_id'] = 'admin_gilang'
            refresh['email'] = 'gilang@example.com'
            request.session.modified = True
            request.session.save()
            response = redirect('post_list')
            response.set_cookie(
                key='sessionid',
                value=request.session.session_key,
                httponly=True,
                secure=False,  # False di lokal
                samesite='Lax'
            )
            return response
        else:
            return Response({'error': 'Kata kunci salah'}, status=status.HTTP_401_UNAUTHORIZED)

def login_view(request):
    if request.method == "POST":
        secret_key = request.POST.get("secret_key", "").strip()
        
        if check_admin_password(secret_key):
            request.session['is_authenticated'] = True
            request.session['user_id'] = 'admin_gilang'
            request.session['email'] = 'gilang@example.com'
            request.session.modified = True   # ini wajib biar session di-save!
            request.session.save()            # force save sekarang juga
            print("DEBUG SESSION SET:", dict(request.session))  # liat di terminal
            messages.success(request, "berhasl login~")
            return redirect('post_list')
        else:
            messages.error(request, "Kata kuncinya beda nih~ Coba lagi")
    
    return render(request, 'page/login.html')

def logout_view(request):
    request.session.flush()
    messages.info(request, "Logout berhasil~ Sampai jumpa lagi!")
    return redirect('login')