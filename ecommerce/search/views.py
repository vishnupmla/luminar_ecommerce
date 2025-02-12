from django.shortcuts import render
from shop.models import Product
from django.db.models import Q # Create your views here.
def searchView(request):
    if request.method == 'POST':
        q = request.POST['q']
        pdct = Product.objects.filter(Q(name__icontains=q) or Q(desc__icontains=q))
        context = {'pdct': pdct, 'qr': q}
    return render(request, 'search.html', context)