from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import *
from .utils import cookieCart,cartData,guestOrder

# def store(request):
#     data=cartData(request)
#     cartItems=data['cartItems']


#     products=Product.objects.all()
#     context={'hello': products,'cartItems':cartItems}
#     return render(request,'store/store.html',context)
from .models import Product, Category

def store(request):
    data = cartData(request)
    cartItems = data['cartItems']

    category_id = request.GET.get('category')
    if category_id:
        products = Product.objects.filter(category_id=category_id)
    else:
        products = Product.objects.all()

    categories = Category.objects.all()

    context = {
        'hello': products,
        'cartItems': cartItems,
        'categories': categories,
        'selected_category': int(category_id) if category_id else 0,
    }
    return render(request, 'store/store.html', context)

def cart(request):

    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']
        
        


    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/cart.html',context)

def checkout(request):
    

    data=cartData(request)
    cartItems=data['cartItems']
    order=data['order']
    items=data['items']

    context={'items':items,'order':order,'cartItems':cartItems}
    return render(request,'store/checkout.html',context)


def updateItem(request):
    data=json.loads(request.body)
    productID=data['productID']
    action=data['action']
    print('Action:',action)
    print('productID:',productID)

    customer=request.user.customer
    product=Product.objects.get(id=productID)
    order,created=Order.objects.get_or_create(customer=customer,complete=False)

    orderItem,created=OrderItem.objects.get_or_create(order=order,product=product)

    if action=='add':
        orderItem.quantity=(orderItem.quantity+1)
    
    elif action=='remove':
        orderItem.quantity=(orderItem.quantity-1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added',safe=False)


def processOrder(request):
    transaction_id=datetime.datetime.now().timestamp()
    data=json.loads(request.body)

    if request.user.is_authenticated:
        customer=request.user.customer
        order,created=Order.objects.get_or_create(customer=customer,complete=False)


        

    else:
        customer, order = guestOrder(request, data)
       

    total=float(data['form']['total'])
    order.transaction_id=transaction_id

    if total == float(order.get_cart_total):
        order.complete=True
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data['shipping']['address'],
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode'],

            )

    return JsonResponse('Payment Complete!', safe=False)

def intro(request):
    return render(request,'store/intro.html')

def about(request):
    return render(request,'store/About_us.html')