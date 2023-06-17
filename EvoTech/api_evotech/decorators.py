from django.shortcuts import redirect
from functools import wraps
from .models import User

def custom_login_required(view_func):
    @wraps(view_func)
    def wrapper(request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(idUser=user_id)
            # Add your authentication logic here
            if user.is_authenticated:
                return view_func(request,user_id, *args, **kwargs)
        except User.DoesNotExist:
            return redirect('index')  # Handle the case when the user doesn't exist or is not authenticated

        return redirect('login')  # Replace 'login' with your login URL

    return wrapper

def admin_required(role):
    def decorator(view_func):
      def wrapper(request, user_id, *args, **kwargs):
        try:
            user = User.objects.get(idUser=user_id)
            # Add your authentication logic here
            if user.profile == role:
                return view_func(request, user_id, *args, **kwargs)
        
        except User.DoesNotExist:
            return redirect('index')  # Handle the case when the user doesn't exist or is not authenticated
        
        return redirect('login')  # Replace 'login' with your login URL
      
      return wrapper  
    return decorator
