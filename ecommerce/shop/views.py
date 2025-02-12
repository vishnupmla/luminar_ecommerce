from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Category, Product
from django.views.generic import DetailView, CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.urls import reverse_lazy
# Create your views here.
def homeView(request):
    cat = Category.objects.all()
    context = {'cat':cat}
    return render(request,'category.html',context)

class ProductDetail(DetailView):
    model = Category
    template_name = 'product.html'
    context_object_name = 'cat'

class SingleProductDetail(DetailView):
    model = Product
    template_name = 'singleproduct.html'
    context_object_name = 'pdct'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        product = self.get_object()
        category = product.category

        context['cat'] = category
        return context

def userRegister(request):
    if request.method  == 'POST':
        fn = request.POST['fn']
        ln = request.POST['ln']
        un = request.POST['un']
        em = request.POST['em']
        p1 = request.POST['p1']
        p2 = request.POST['p2']

        if p1 == p2:
            usr = User.objects.create_user(username=un,first_name=fn,last_name=ln,email=em,password=p1)
            print(usr.save())
            return redirect('shop:home')
        else:
            messages.error(request,'Password mismatch')
    return render(request,'register.html')

def userLogin(request):
    if request.method == 'POST':
        un = request.POST['un']
        passwd = request.POST['paswd']
        usr = authenticate(username =un, password = passwd)
        if usr:
            login(request,usr)
            print('success')
            return redirect('shop:home')
        else:
            messages.error(request,'Invalid username or password')

    return render(request,'login.html')

@login_required
def userLogout(request):
    logout(request)
    return redirect('shop:login')

@login_required
def trackOrders(request):
    return render(request,'trackorders.html')

def aboutUs(request):
    return render(request,'about.html')

class AddCategory(CreateView):
    model = Category
    template_name = 'addcategory.html'
    fields = '__all__'
    success_url = reverse_lazy('shop:home')

class AddProduct(CreateView):
    model = Product
    template_name = 'addproduct.html'
    fields = ['name','desc','image','price','stock','category']
    success_url = reverse_lazy('shop:home')

class AddStock(UpdateView):
    model = Product
    fields = ['stock']
    template_name = 'addstock.html'
    # success_url = reverse_lazy('shop:home')
    def get_success_url(self):
        return reverse_lazy('shop:productdetails',kwargs={'pk':self.object.id})