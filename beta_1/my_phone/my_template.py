def temp(request):
    return {"key": request.COOKIES.get("theme")}


def temp1(request):
    return {"key1": "привет!!!!"}
