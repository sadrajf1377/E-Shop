from django.http import JsonResponse


def login_required_api(func):
    def wrapper(*args):
        is_authenticated=args[0].user.is_authenticated
        if is_authenticated:
            print('user is authenticated')
            return func(*args)
        else:
            print('user is not authenticated')
            return JsonResponse({'error':'برای دسترسی به این بخش ابتدا وارد شوید'},status=403)
    return wrapper