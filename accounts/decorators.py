from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view) :
    def wrappper_func(request, *args, **kwargs) :
        if request.user.is_authenticated :
            return redirect('/')
        else :
            return view(request, *args, **kwargs)
    
    return wrappper_func

def allowed_users(allowed_roles=[]) :
    def decorator(view) :
        def wrappper_func(request, *args, **kwargs) :
            # print(allowed_roles)

            user_group = None
            if request.user.groups.exists() :
                user_group = request.user.groups.all()[0].name
            
            if user_group in allowed_roles :
                return view(request, *args, **kwargs)
            else :
                return HttpResponse("You are not authorized to view this page!!!")
        return wrappper_func
    return decorator

def admin_only(view) :
    print("admin only")
    def wrappper_func(request, *args, **kwargs) :
        user_group = None

        if request.user.groups.exists() :
            user_group = request.user.groups.all()[0].name
        print("yes", user_group)
        if user_group == 'admin' :
            return view(request, *args, **kwargs)
        
        if user_group == 'customer' :
            return redirect('userHome/')

    return wrappper_func