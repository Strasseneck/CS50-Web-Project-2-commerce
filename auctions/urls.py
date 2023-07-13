from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("save_listing",views.save_listing, name="save_listing"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("add_watchlist", views.add_watchlist, name="add_watchlist"),
    path("remove_watchlist", views.remove_watchlist, name="remove_watchlist"),
    path('watchlist', views.watchlist, name="watchlist"),
    path('place_bid', views.place_bid, name="place_bid"),
    path('add_comment', views.add_comment, name="add_comment"),
    path('categories', views.categories, name="categories"),
    path('category_listings/<str:title>', views.category_listings, name="category_listing"),
    path('close_listing', views.close_listing, name="close_listing")
    
]
