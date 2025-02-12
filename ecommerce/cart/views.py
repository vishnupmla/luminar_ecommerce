import razorpay
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render,redirect
from django.views.decorators.csrf import csrf_exempt
from shop.models import Product
from .models import Cart,OrderDetails,Payment


# Create your views here.
@login_required
def addToCart(request,i):
    usr = request.user  #User Details
    p = Product.objects.get(id=i)
    try:
        ct = Cart.objects.get(user=usr,product=p)
        if p.stock >0:
            ct.quantity += 1
            ct.save()
            p.stock -= 1
            p.save()
    except:
        c = Cart.objects.create(user=usr,product=p,quantity=1)
        c.save()
        p.stock -= 1
        p.save()
    return redirect('cart:cartview')

@login_required
def cartView(request):
    usr = request.user
    ct = Cart.objects.filter(user=usr)
    print(ct)
    ttl = cartTotal(request)
    context = {'ct':ct,'ttl':ttl}
    return render(request,'cart.html',context)

@login_required
def delCartItem(request,i):
    p = Product.objects.get(id=i)
    u =request.user
    try:
        item = Cart.objects.get(user=u,product=p)
        qn = item.quantity
        item.delete()

        p.stock += qn
        p.save()
    except:
        pass
    return redirect('cart:cartview')
@login_required
def decrCart(request,i):
    p = Product.objects.get(id=i)
    u = request.user
    try:
        item = Cart.objects.get(user=u,product=p)
        if item.quantity > 1:
            item.quantity -= 1
            item.save()
            p.stock += 1
            p.save()
        else:
            item.delete()
            p.stock += 1
            p.save()
        return redirect('cart:cartview')
    except:
        pass

@login_required
def updateCart(request,i):
    pass

def cartTotal(request):
    u = request.user
    p = Cart.objects.filter(user=u)
    total = 0
    for i in p:
       total += i.quantity * i.product.price
    return total

def checkout(request):
    usr = request.user
    ct = Cart.objects.filter(user=usr)
    ttl = int(cartTotal(request))

    if request.method == 'POST':
        addr = request.POST['addr']
        phone = request.POST['ph']
        pin = request.POST['pin']

        clnt = razorpay.Client(auth=('rzp_test_EhsaYzYBls8rCV','3lAxJtKEpEr9SpasaYbwU15L'))
        response_payment = clnt.order.create(dict(amount=ttl*100,currency='INR'))
        print(response_payment)
        order_id = response_payment['id']
        status = response_payment['status']

        if status == 'created':
            p = Payment.objects.create(name=usr.username,amount=ttl,order_id=order_id)
            p.save()

            for i in ct:
                o = OrderDetails.objects.create(product=i.product,user=i.user,phone=phone,address=addr,pin=pin,order_id=order_id,no_of_items=i.quantity)
                o.save()

            context = {'payment':response_payment,'name':usr.username}
            return render(request,'payment.html',context)

    context = {'ct': ct, 'ttl': ttl,'usr':usr}
    return render(request,'checkout.html',context)

@csrf_exempt
def paymentStatus(request,i):
    usr = User.objects.get(username=i)
    login(request,usr)

    response = request.POST
    print(response)

    #To check the validity of the razor_pay payment details
    param_dict = {
        'razorpay_order_id':response['razorpay_order_id'],
        'razorpay_payment_id':response['razorpay_payment_id'],
        'razorpay_signature':response['razorpay_signature']
    }
    clnt = razorpay.Client(auth=('rzp_test_EhsaYzYBls8rCV','3lAxJtKEpEr9SpasaYbwU15L'))
    try:
        status = clnt.utility.verify_payment_signature(param_dict)
        print(status)
        py =Payment.objects.get(order_id=response['razorpay_order_id'])
        py.paid =True
        py.razorpay_payment_id = response['razorpay_payment_id']
        py.save()

        o = OrderDetails.objects.filter(order_id=response['razorpay_order_id'])
        for i in o:
            i.payment_status = 'completed'
            i.save()

        c = Cart.objects.filter(user=usr)
        c.delete()
    except:
        pass
    return render(request,'status.html')

def orderView(request):
    usr = request.user
    o = OrderDetails.objects.filter(user=usr,payment_status='completed')
    return render(request,'yourorders.html',{'o':o})

