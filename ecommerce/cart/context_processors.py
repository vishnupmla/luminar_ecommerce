from .models import Cart
def cartcount(request):
    try:
        u = request.user
        c = Cart.objects.filter(user=u)
        cnt = len(c)
        return {'count':cnt,'usr':u}
    except:
        return {'count':0}