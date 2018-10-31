from django.http import JsonResponse


def index(request):
    return JsonResponse({"name": "lhr", "sex": "nan"})


