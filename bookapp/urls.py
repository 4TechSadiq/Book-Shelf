from django.urls import path
from . import views

urlpatterns = [
    path("create-book/",views.createBook,name="createbook"),
    path("",views.listBook,name="booklist"),
    path("adbook/<int:book_id>",views.detailsview,name="bookdetails"),
    path("updateview/<int:book_id>",views.updateBook,name="update"),
    path("delete/<int:book_id>",views.deleteView,name="delete"),
    path("authorview/",views.CreateAuthor,name="author"),
    path("index/",views.index),
    path("search/", views.searchBook,name="search"),
    path("signup/",views.registerUser,name="signup"),
    path("login/", views.loginUser,name="login"),
    path("logout",views.logOut,name="logout"),
]