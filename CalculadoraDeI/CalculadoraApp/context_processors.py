from .models import Perfil 

def user_info(request):
    user_data = {}
    if request.user.is_authenticated:
        user_data['user_username'] = request.user.username
        try:
            user_data['user_rol'] = request.user.perfil.rol
        except Perfil.DoesNotExist:
            user_data['user_rol'] = 'N/A' 
    return user_data

