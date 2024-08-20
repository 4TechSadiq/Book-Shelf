from django.shortcuts import render, redirect
from .forms import AuthorForm, BookForm
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages,auth
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required

# Create your views here.

from .models import book,Author

# def createBook(request):

#     Books = book.objects.all() 
#     if request.method == "POST":
#         title = request.POST.get("title")
#         price = request.POST.get("price")

#         Book=book(title=title,price=price)
#         Book.save()

#     return render(request,'book.html',{"books":Books})

def createBook(request):
    Book =book.objects.all()
    if request.method == "POST":
        form = BookForm(request.POST,request.FILES)
        if form.is_valid():
            form.save()
            return redirect("booklist")
    else:
        form = BookForm()

    return render(request,'admin/book.html',{'form':form,'books':Book})

def CreateAuthor(request):
    if request.method== "POST":
        form = AuthorForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("createbook")
    else:
        form = AuthorForm()

    return render(request,"admin/author.html",{'form':form})

def listBook(request):
    Books = book.objects.all()
    paginator = Paginator(Books,4)
    page_no =request.GET.get("page")
    print(request.user)
    try:
        page = paginator.get_page(page_no)
    except EmptyPage:
        page = paginator.page(page_no.num_pages)

    return render(request,"admin/listbook.html",{"books":Books,"page":page})


def detailsview(request,book_id):
    Book = book.objects.get(id=book_id)

    return render(request,"admin/detailsview.html",{'book':Book})


def updateBook(request,book_id):
    # Book = book.objects.get(id=book_id)

    # if request.method=="POST":
    #     title = request.POST.get("title")
    #     price = request.POST.get("price")

    #     Book.title=title
    #     Book.price = price

    #     Book.save()
    #     return redirect("/")


    # return render(request,"updateview.html",{"book":Book})

    Book =book.objects.get(id=book_id)

    if request.method=="POST":
        form = BookForm(request.POST,request.FILES,instance=Book)
        if form.is_valid():
            form.save()
            return redirect("/")
    else:
        form = BookForm(instance=Book)

    return render(request,"admin/updateview.html",{'form':form})
    
def deleteView(request,book_id):
    Book = book.objects.get(id=book_id)

    if request.method=="POST":
        Book.delete()

        return redirect("booklist")
    return render(request,"admin/delete.html",{'book':Book})

def index(request):
    return render(request,"admin/base.html")

def searchBook(request):
    query = None
    Books = None

    if "q" in request.GET:
      query = request.GET.get("q") 
      Books = book.objects.filter(Q(title__icontains=query))


    else:
        Books = []

    context = {
        "books": Books,
        "query": query,
    }

    return render(request,"admin/search.html",context)


def combinedSearch(request):
    query = request.GET.get('q', '')
    books = []
    authors = []

    if query:
        Books = book.objects.filter(Q(title__icontains=query))
        authors = Author.objects.filter(Q(name__icontains=query))

    context = {
        'books': books,
        'authors': authors,
        'query': query
    }

    return render(request, 'admin/search.html', context)

# 


def registerUser(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Account created successfully! You can now log in.")
            return redirect("login")
        else:
            # If the form is not valid, show form errors
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("signup")
    
    else:
        form = UserCreationForm()

    return render(request, "admin/register.html", {"form": form})


# def loginUser(request):
#     username = "admin"
#     password = "123"
#     if request.method == "POST":
#         user = request.POST.get("username")
#         pashword = request.POST.get("password")
#         user = auth.authenticate(username=username,password=password)

#         if user is not None:
#             auth.login(request,user)
#             return redirect("booklist")
#         else:
#             messages.info(request,"invalid user")
#             return redirect("login")

#     return render(request,"admin/login.html")


def loginUser(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f"userrrrrrrrrrr {request.user}")
                messages.success(request, "Login successful!")
                return redirect("booklist")  # Redirect to a home or dashboard page
            else:
                messages.error(request, "Invalid username or password.")
                return redirect("login")
        else:
            # If the form is not valid, show form errors
            for error in form.errors.values():
                messages.error(request, error)
            return redirect("login")
    
    else:
        form = AuthenticationForm()

    return render(request, "admin/login.html", {"form": form})

@login_required
def logOut_user(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect("login")
