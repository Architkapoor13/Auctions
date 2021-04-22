from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.newlisting, name="newlisting"),
    path("listings/<int:listing_code>", views.listing, name="listings"),
    path("watchlist", views.userwatchlist, name = "userwatchlist"),
    path("closelisting", views.close, name = "close"),
    path("closemsg/<int:listing_code>", views.isclosedmsg, name="message"),
    path("alllistings", views.alllistings, name="alllistings"),
    path("comments", views.comments, name="comments"),
    path("categories", views.categories, name="categories"),
    path("category/<str:cat>", views.category, name="category"),
    path("mylistings", views.mylistings, name="mylistings")
]
