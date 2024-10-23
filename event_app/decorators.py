from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)

    return wrapper_func

def staff_check(view_func):
    def wrapper_func(request, *args, **kwargs):
        if not request.user.is_staff:
            return redirect("home")
        else:
            return view_func(request, *args, **kwargs)
        
    return wrapper_func
