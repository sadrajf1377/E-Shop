from django.http import JsonResponse


def login_required_api(func):
    def wrapper(*args):
        is_authenticated=args[0].user.is_authenticated
        if is_authenticated:
            return func(*args)
        else:
            return JsonResponse({'error':'برای دسترسی به این بخش ابتدا وارد شوید'},status=403)
    return wrapper