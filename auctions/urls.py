from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("listing", views.listing_view, name="listing"),
    path("listing_page/<str:id>", views.listing_page, name="listing_page"),
    path("add_listing/<str:id>", views.add_listing, name="add_listing"),
    path("bid/<str:id>", views.bid, name="bid"),
    path("close_listing/<str:id>", views.close_listing, name="close_listing"),
    path("add_comments/<str:id>", views.add_comment, name="add_comment"),
    path("watchlist", views.watchlist, name="watchlist"),
    path("remove_listing/<str:id>", views.remove_listing, name="remove_listing"),
    path("listing_categories", views.listing_categories, name="listing_categories"),
    path("category_listings/<str:category>", views.category_listings, name="category_listings"),
    path("my_listing", views.my_listing, name="my_listing")
]
