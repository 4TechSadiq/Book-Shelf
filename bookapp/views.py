from django.shortcuts import render, redirect
from .forms import AuthorForm, BookForm
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib import messages,auth

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

def registerUser(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        repassword = request.POST.get("re-password")

        if password == repassword:
            if User.objects.filter(username=name).exists():
                messages.info(request,"Username already exist")
                return redirect("signup")
            elif User.objects.filter(email=email).exists():
                messages.info(request,"email already taken")
                return redirect("signup")
            else:
                user = User.objects.create_user(username=name,email=email,password=password)
                user.save()
            return redirect("login")
        else:
            messages.info(request,"password doesnt match try again")
            return redirect("signup")
    
    return render(request,"admin/register.html")

def loginUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect("booklist")
        else:
            messages.info(request,"invalid user")
            return redirect("login")

    return render(request,"admin/login.html")

def logOut(request):
    auth.logout(request)
    return redirect("login")
