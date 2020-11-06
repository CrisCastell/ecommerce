from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .decorators import unathenticated_user, allowed_users
from .forms import UpdateCustomerForm
from .models import Customer, Product, Order, Item, Shipping, ProductImage, SlideProduct
import json

# Create your views here.
def home(request):
    slideProducts = SlideProduct.objects.all()[:4]
    products = Product.objects.all()
    best = Product.objects.filter(category='BS')[:8]
    new = Product.objects.filter(category='N')[:8]
    discount = Product.objects.filter(category='D')[:8]
    context = {'products':products, 'best':best, 'new':new, 'discount':discount, 'slide':slideProducts, 'last':slideProducts[3], 'first':slideProducts[0]}
    return render(request, 'store/index.html', context)



def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.item_set.all()
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
            print(cart)
        except:
            cart = {}

        items = []

        for i in cart:
            
            try:
                product = Product.objects.get(id=i)
                item = {
                    'product':{
                        'id':product.id,
                        'name':product.name,
                        'price':product.price,
                        'image':product.image,
                    },
                    'quantity':cart[i]['quantity'],
                }
                
                items.append(item)
            except:
                pass
        
    context = {'items':items}
    return render(request, 'store/cart.html', context)

def checkout(request):
    return render(request, 'store/checkout.html',)


def category(request, name):
    products = Product.objects.filter(category=name)
    context = {'products':products}
    return render(request, 'store/category.html', context)

def detailView(request, id):
    product = get_object_or_404(Product, id=id)
    images = ProductImage.objects.filter(product=product)
    similar = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    context = {'product':product, 'similar':similar, 'images':images}
    return render(request, 'store/detail-view.html', context)



#Update and see user profile
@login_required(login_url='login')
def profile(request):
    user = request.user.customer
    form = UpdateCustomerForm(instance=user)
    if request.method == 'POST':
        form = UpdateCustomerForm(request.POST, request.FILES , instance=user)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('profile'))
    context = {'form':form}
    return render(request, 'store/profile.html', context)






#Authentication views

@unathenticated_user
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "store/login.html", {
                "message": "Invalid username and/or password."
            })
    return render(request, 'store/login.html')




@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))



@unathenticated_user
def register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")

        # Ensure password matches confirmation
        password = request.POST.get("password")
        confirmation = request.POST.get("confirmation")
        if password != confirmation:
            return render(request, "store/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "store/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("home"))
    else:
        return render(request, "store/register.html")


#Api
def updateOrder(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    
    data = json.loads(request.body)
    print(data)
    action = data['action']
    product = get_object_or_404(Product, id=int(data['productId']))
    
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer, complete=False)
    orderItem, created = Item.objects.get_or_create(order=order, product=product)
    
    deleted = False
    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()
        deleted = True

    response = {'deleted': deleted, 'quantity': orderItem.quantity, 'id':orderItem.product.id}
    return JsonResponse(response, status=201)




def orderInfo(request):
    response = {
        'totalItems':0,
        'subtotal':0
    }
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        response['totalItems'] = order.get_cart_items
        response['subtotal'] = order.get_cart_total
        
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        
        except:
            cart = {}
        for i in cart:
            product = Product.objects.get(id=i)
            subtotal = (product.price * cart[i]['quantity'])

            response['totalItems'] += cart[i]['quantity']
            response['subtotal'] += subtotal
        
    
    return JsonResponse(response, safe=False)


def processOrder(request):
    if request.method != 'POST':
        return JsonResponse({"error": "POST request required."}, status=400)
    data = json.loads(request.body)
    
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        
        order.complete = True

        order.save()

        
    else:
        try:
            cart = json.loads(request.COOKIES['cart'])
        except:
            cart = {}
        
        customer, created = Customer.objects.get_or_create(
            username=f"{data['data']['name']}-guest",
            email= data['data']['email'])
        customer.save()


        order = Order.objects.create(customer=customer, complete=False)
        for i in cart:
            try:
                product = Product.objects.get(id=i)

                orderItem = Item.objects.create(
                    product=product,
                    quantity=cart[i]['quantity'],
                    order=order)
            except:
                pass
        
        order.complete = True

        order.save()
    Shipping.objects.create(
            order=order,
            customer=customer,
            address=data['data']['address'],
            city=data['data']['city'],
            state=data['data']['state'],
            zip_code=data['data']['zipCode'] 
        )
    return JsonResponse({'message':'Order processed succesfully'}, status=201)

@allowed_users(allowed_roles=['admin'])
def shippings(request):
    if request.method == 'POST':
        shipData = json.loads(request.body)
        shipping = Shipping.objects.get(id=shipData['id'])
        shipping.delivered = True
        shipping.save()
    
    pendingShipping = Shipping.objects.filter(delivered=False)
    data = []
    for shipping in pendingShipping:
        order = shipping.order
        shipping = {
            'shipping':shipping.serialize(),
            'orderTransaction':order.transaction,
            'customer':{
                'username':shipping.customer.username,
                'email':shipping.customer.email
            },
            'items':[item.serialize() for item in order.item_set.all()]
        }

        data.append(shipping)
    return JsonResponse(data, safe=False)

@allowed_users(allowed_roles=['admin'])
def adminControl(request):
    return render(request, 'store/admin-view.html')