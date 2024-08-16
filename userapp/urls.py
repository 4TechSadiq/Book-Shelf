from django.urls import path
from . import views


urlpatterns = [
    path("userpage/",views.userapp,name="index"),
    path("details/<int:book_id>",views.detailsview,name="details"),
    path("searchBook/",views.searchUserBook,name="searchBook"),
    path("",views.register,name="signup"),
    path("login/",views.user_login,name="login"),
    path("add_to_cart/<int:book_id>/", views.add_to_cart, name="addtocart"),
    path("viewcart/",views.viewCart, name="viewcart"),
    path("increase/<int:item_id>/", views.increase_quantity,name="increase_quantity"),
    path("decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("remove/<int:item_id>/", views.remove_from_cart,name="remove_cart"),
    path("create-checkout-session/", views.checkout_session, name="create-checkout-session"),
    path("success/", views.success, name="success"),
    path("logout/",views.logout,name="logout"),
    path("cancel/", views.cancel, name="cancel"),
]
