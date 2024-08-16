from django.shortcuts import render,redirect, HttpResponseRedirect
from bookapp.models import book
from .models import Cart, CartItem, CustomUser
from django.core.paginator import Paginator,EmptyPage
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib import messages
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from django.contrib.auth.forms import AuthenticationForm

# Create your views here.

def listBook(request):
    Books = book.objects.all()
    paginator = Paginator(Books,4)
    page_no =request.GET.get("page")
    try:
        page = paginator.get_page(page_no)
    except EmptyPage:
        page = paginator.page(page_no.num_pages)

    return render(request,"listbook.html",{"books":Books,"page":page})

@login_required
def logout(request):
    request.session.flush()
    return redirect("login")

@login_required
def userapp(request):
    Books = book.objects.all()
    #print(request.user)
    paginator = Paginator(Books,8)
    page_no = request.GET.get("page")
    try:
        page = paginator.get_page(page_no)
    except:
        page = paginator.page(page_no.num_pages)
    return render(request,"user/userpage.html",{"books":Books,"page":page})


def detailsview(request,book_id):
    Books = book.objects.get(id=book_id)
    return render(request,"user/details.html",{"books":Books})

def searchUserBook(request):
    query = None
    Books = None

    if "q" in request.GET:
        query = request.GET.get("q")
        Books = book.objects.filter(Q(title__icontains=query))
    else:
        Books = []

    context = {
        "books": Books,
        "query": query
    }
    return render(request,"user/searchUserBook.html",context)

# def UserRegistration(request):
#     userprofile = UserTable()
#     login_table = LoginTable()

#     if request.method == "POST":
#         # username = request.POST["username"]
#         # email = request.POST["email"]
#         # password = request.POST["password"]
#         # rpassword = request.POST["rpassword"]

#         userprofile.username = request.POST["username"]
#         userprofile.password = request.POST["password"]
#         userprofile.rpassword = request.POST["password"]
#         userprofile.email = request.POST["email"]
        
#         login_table.username = request.POST["username"]
#         login_table.password = request.POST["password"]
#         login_table.rpassword = request.POST["password"]
#         login_table.email = request.POST["email"]
#         login_table.userType = "user"

#         if request.POST["password"] == request.POST["rpassword"]:
#             userprofile.save()
#             login_table.save()
#             messages.info(request,"Signup Successful")
#             return redirect("login")
#         else:
#             messages.info(request,"Password doesnt match")
#             return redirect("signup")
    
#     return render(request,"user/signup.html")

# def loginUser(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         print(username, password)
#         user = LoginTable.objects.filter(username=username,password=password).exists()
#         #user = authenticate(request, username=username, password=password)
#         print(user)
#         try:
#             if user is not None:
#                 #login(request,user)
#                 user_details = LoginTable.objects.filter(username=username,password=password)
#                 user_name = user_details.username
#                 user_type = user_details.userType
#                 print(request.user)

#                 if user_type == "user":
#                     request.session["username"] = user_name
#                     return redirect("index")
#                 elif user_type == "admin":
#                     request.session["username"] = user_name
#                     return redirect("bookadmin")
#             else:
#                 messages.error(request,"Invalid user or password")
#         except EmptyPage:
#             messages.error(request,"invalid role")   

#     return render(request,"user/login.html")

# def loginUser(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         print(username, password)

#         # Check if any user exists with the given username and password
#         users = LoginTable.objects.filter(username=username, password=password)
        
#         if users.exists():
#             user_details = users.first()  # Get the first matching record
#             user_name = user_details.username
#             user_type = user_details.userType
#             print(request.user)

#             if user_type == "user":
#                 request.session["username"] = user_name
#                 return redirect("index")
#             elif user_type == "admin":
#                 request.session["username"] = user_name
#                 return redirect("bookadmin")
#         else:
#             messages.error(request, "Invalid username or password")

#     return render(request, "user/login.html")


# def UserRegistration(request):
#     if request.method == "POST":
#         username = request.POST["username"]
#         password = request.POST["password"]
#         password2 = request.POST["password"]
#         email = request.POST["email"]
        
#         if password == password2:
#             user = authenticate(username=username, password=password, email=email)
#             if user is not None:
#                 login(request, user)
#                 print(request.user)
#             else:
#                 messages.error(request,"error occured")
#         else:
#             messages.error(request,"password doesnt match")
#     return render(request,"user/signup.html")
# def loginUser(request):
#     if request.method == "POST":
#         pass

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("index")
    else:
        form = CustomUserCreationForm()
    return render(request, "user/signup.html", {"form": form})

def user_login(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        #print(form.as_p())
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect("index")
    else:
        form = AuthenticationForm()
    return render(request, "user/login.html", {"form": form})


def add_to_cart(request, book_id):
    Book = book.objects.get(id=book_id)
    if Book.quantity>0:
        cart,created = Cart.objects.get_or_create(user=request.user)
        cart_item, item_created = CartItem.objects.get_or_create(cart=cart, Book=Book)

        if not item_created:
            cart_item.quantity+=1
            cart_item.save()
    return redirect('viewcart')

# def add_to_cart(request, book_id):
#     Book = book.objects.get(id=book_id)
#     username = request.session.get("username")
#     user = CustomUser.objects.get(email=request.user)
#     # print(request.session.get("username"))
#     # print(f" this is {request.user}")
#     if Book.quantity > 0 :
#         cart, created = Cart.objects.get_or_create(request.user)
#         cart_item,item_created = CartItem.objects.get_or_create(cart=cart, Book=Book)

#         if not item_created:
#             cart_item.quantity+=1
#             cart_item.save()
#     return redirect("viewcart")

def viewCart(request):
    cart,created = Cart.objects.get_or_create(user=request.user)
    cart_items = cart.cartitem_set.all()
    cart_item = CartItem.objects.all()
    total_price = sum(item.Book.price * item.quantity for item in cart_items)
    total_items = cart_items.count()

    context = {
        "cart_items": cart_items,
        "cart_item": cart_item,
        "total_price": total_price,
        "total_item": total_items
    }
    return render(request,"user/cart.html", context)

    

def increase_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item < cart_item.Book.quantity:
        cart_item.quantity += 1
        cart_item.save()
    return redirect("viewcart")

def decrease_quantity(request,item_id):
    cart_item = CartItem.objects.get(id=item_id)
    if cart_item.quantity >1:
        cart_item.quantity -= 1
        cart_item.save()
    return redirect("viewcart")

def remove_from_cart(request,item_id):
    try:
        cart_item = CartItem.objects.get(id=item_id)
        cart_item.delete()
    except cart_item.DoesNotExist:
        pass
    return redirect("viewcart")


# def create_checkout_session(request):
#     cart_items = CartItem.objects.all()


#     if cart_items:
#         stripe.api_key = settings.STRIPE_SECRET_KEY
#         if request.method == "POST":
#             line_items = []
#             print("heeeeeeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
#             for cart_item in cart_items:
#                 if cart_item.Book:  
#                     line_item = {
#                         "price_data": {
#                             "currency": "INR",
#                             "unit_amount": int(cart_item.Book.price * 100),
#                             "product_data": {
#                                 "name": cart_item.Book.title
#                             },
#                         },
#                         "quantity": cart_item.Book.quantity  
#                     }
#                     line_items.append(line_item)

#             if line_items:
#                 checkout_session = stripe.checkout.Session.create(
#                     payment_method_types=['card'],
#                     line_items=line_items,
#                     mode='payment',
#                     success_url=request.build_absolute_uri(reverse('success')),
#                     cancel_url=request.build_absolute_uri(reverse('cancel'))
#                 )
#                 print("heeeeeeeeeeeeeeeeeeyyyyyyyyyyyyyyyyyyyyyyyyyyyyy")
#                 return redirect(checkout_session.url, code=303)



def checkout_session(request):
    cart_items=CartItem.objects.all()

    if cart_items:
        stripe.api_key=settings.STRIPE_SECRET_KEY

        if request.method=='POST':
            line_items=[]

            for cart_item in cart_items:
                if cart_item.Book:
                    line_item={
                        'price_data':{
                            'currency':'INR',
                            'unit_amount':int(cart_item.Book.price * 100),
                            'product_data':{
                                'name':cart_item.Book.title
                            },
                        },
                        'quantity':cart_item.quantity
                    }
                    line_items.append(line_item)

            if line_items:
                checkout_session=stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel')),
                )

                return redirect(checkout_session.url,code=303)
        
def success(request):
    cart_items = CartItem.objects.all()
    for cart_item in cart_items:
        product = cart_item.Book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()
    
    cart_items.delete()
    return render(request,"user/success.html")

def cancel(request):
    return render(request, "user/cancel.html")