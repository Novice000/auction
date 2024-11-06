from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.db.models import Max

from .models import User, Listings, Bids, Comments, WatchList, Winners
from .forms import ListingsForm, BidForm, CommentForm

def index(request):
    # Fetch all active listings, annotating each with its highest bid for easy reference        
    active = Listings.objects.filter(closed=False).annotate(highest_bid=Max("bids__price"))
    if request.user.is_authenticated:
        my_bids = Bids.objects.filter(user__id=int(request.user.id)).select_related("listing")
    else:
        my_bids = None
    return render(request, "auctions/index.html", {"active": active,
                                                    "my_bids": my_bids})
    


def login_view(request):
    if request.method == "POST":
        # Authenticate user with provided username and password
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication is successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            # Provide error message for invalid login credentials
            return render(request, "auctions/login.html", {"message": "Invalid username and/or password."})
    return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]

        # Check if passwords match
        if password != confirmation:
            return render(request, "auctions/register.html", {"message": "Passwords must match."})

        try:
            # Attempt to create a new user and handle potential IntegrityError if username is taken
            user = User.objects.create_user(username, email, password)
            user.save()
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        except IntegrityError:
            # Provide error message for duplicate username
            return render(request, "auctions/register.html", {"message": "Username already taken."})

    return render(request, "auctions/register.html")


@login_required
def listing_view(request):
    if request.method == "POST":
        form = ListingsForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.user = request.user 
            listing.save()
            return redirect(reverse("index"))
        else:
            # Provide error message if form data is invalid
            return render(request, "auctions/listing.html", {"form": form, "error": "Invalid form data."})
    return render(request, "auctions/listing.html", {"form": ListingsForm()})


def listing_page(request, id):
    # Fetch the listing or raise a 404 if it doesn’t exist
    listing = get_object_or_404(Listings, pk=id)
    comments = Comments.objects.filter(listing=listing)
    highest_bid = listing.bids.aggregate(highest_bid=Max("price"))["highest_bid"]
    bid_form = BidForm(highest_bid=highest_bid)
    comment_form = CommentForm()
    if highest_bid == None:
        winner = None
    elif listing.closed:
        if Winners.objects.filter(listing=listing).exists():
            winning = Winners.objects.get(listing=listing)
            winner = (winning.winner == request.user)
    else:
        winner = None
    
    
    # Check if the user is authenticated and if the listing is on their watchlist
    watched = WatchList.objects.filter(listing=listing, user=request.user).exists() if request.user.is_authenticated else False
    watchlist_id = WatchList.objects.get(listing=listing, user=request.user) if watched else None
    # Check if the current user is the creator of the listing
    creator = request.user.is_authenticated and (listing.user.id == request.user.id)
    my_bid = Bids.objects.filter(user__id=request.user.id, listing__id =int(id) )
    
    return render(request, "auctions/listing_page.html", {
        "listing": listing,
        "comments": comments,
        "bid_form": bid_form,
        "comment_form": comment_form,
        "watched": watched,
        "creator": creator,
        "highest_bid": highest_bid,
        "my_bid": my_bid,
        "winner": winner,
        "watchlist_id": watchlist_id,
    })

@login_required
def bid(request, id):
    # Fetch the listing or raise a 404 if it doesn’t exist
    listing = get_object_or_404(Listings, pk=id)
    bid_form = BidForm(request.POST or None)

    if bid_form.is_valid():
        price = bid_form.cleaned_data["price"]
        # Retrieve the highest bid or default to the initial bid if none exist
        highest_bid = listing.bids.aggregate(highest_bid=Max("price"))["highest_bid"] or listing.initial_bid
        # Ensure the bid is higher than the current highest bid
        if price > highest_bid:
            Bids.objects.create(listing=listing, user=request.user, price=price)
            return redirect("listing_page", id=id)
        else:
            # Show error if bid is too low
            return render(request, "auctions/listing_page.html", {
                "listing": listing,
                "error": "Bid must be higher than the current highest bid.",
                "bid_form": bid_form,
            })
    return redirect("index")


@login_required
def close_listing(request, id):
    # Fetch the listing or raise a 404 if it doesn’t exist
    listing = get_object_or_404(Listings, pk=id)
    # Only allow the listing creator to close it
    if listing.user != request.user:
        return HttpResponse("Unauthorized", status=403)
    listing.closed = True
    listing.save()
    
    # Find the highest bid and create a winner if one exists
    highest_bid = listing.bids.order_by('price').first()
    if highest_bid:
        Winners.objects.create(listing=listing, user=highest_bid.user)
    return redirect("listing_page", id=id)


@login_required
def add_comment(request, id):
    # Fetch the listing or raise a 404 if it doesn’t exist
    listing = get_object_or_404(Listings, pk=id)
    comment_form = CommentForm(request.POST or None)

    if comment_form.is_valid():
        Comments.objects.create(listing=listing, user=request.user, comment=comment_form.cleaned_data["comment"])
        return redirect("listing_page", id=id)
    return HttpResponse("Invalid comment form", status=400)


@login_required
def watchlist(request):
    # Fetch all items in the user’s watchlist
    watchlist_items = WatchList.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html", {"watchlist": watchlist_items})

@login_required
def add_listing(request, id):
    user = request.user
    # Fetch the listing or raise a 404 if it doesn’t exist
    listing = get_object_or_404(Listings, pk=id)
    # Attempt to add listing to the user’s watchlist, preventing duplicates
    watch, created = WatchList.objects.get_or_create(user=user, listing=listing)
    if not created:
        return redirect("listing_page", id=id)  # Already exists in watchlist
    return redirect("watchlist")

@login_required
def remove_listing(request, id):
    # Fetch the specific watchlist item or raise a 404 if it doesn’t exist
    listing = get_object_or_404(WatchList, pk=int(id), user=request.user)
    listing.delete()
    return redirect("index")


def listing_categories(request):
    # Fetch distinct categories from listings
    categories = Listings.objects.values_list("category", flat=True).distinct()
    return render(request, "auctions/category.html", {"categories": categories})


def category_listings(request, category):
    # Fetch listings under the specified category
    listings = Listings.objects.filter(category=category, closed=False).annotate(highest_bid=Max("bids__price"))
    return render(request, "auctions/category_listings.html", {"listings": listings})

@login_required
def my_listing(request):
    listings = Listings.objects.filter(user=request.user).annotate(highest_bid=Max("bids__price"))
    return render(request, "auctions/my_listing.html", {"listings": listings })