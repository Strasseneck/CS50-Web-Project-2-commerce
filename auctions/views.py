from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.db.models import Count
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User
from auctions.models import Listing, Watchlist, Bid, Comment, Seller


def index(request):
    # Get data for watchlist badge
    if request.user.is_authenticated:
        current_user = request.user.id
        count = Watchlist.objects.filter(owner=current_user).count()
        return render(request, "auctions/index.html", {
        "listings": Listing.objects.all(),
        "count": count
        })
    else:
        return render(request, "auctions/index.html", {
        "listings": Listing.objects.all()
        })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))

def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    return render(request, "auctions/new_listing.html")

@login_required
def save_listing(request):
    if request.method == "POST":

        # Get data from form
        title = request.POST["title"]
        description = request.POST["description"]
        img = request.POST["img_url"]
        starting_bid = request.POST["starting_bid"]
        category = request.POST["category"] 
        seller = User.objects.get(username=request.user.username)

        # Save listing
        listing = Listing(title=title,description=description,img_url=img,price=starting_bid,category=category,seller=seller)
        listing.save()
        return render(request, "auctions/index.html")

def listing(request, title):
    listing = Listing.objects.get(title=title) 
    return render(request, "auctions/listing.html", {
        "listing": listing
    })

@login_required
def add_watchlist(request):
    if request.method == "POST":

        # Get data from form
        title = request.POST['title']
        listing = Listing.objects.get(title=title) 
        item = listing
        owner = User.objects.get(username=request.user.username)
        watchlist = Watchlist(owner=owner, item=item)

        # Save watchlist item
        watchlist.save()
        return render(request, "auctions/listing.html", {
        "listing": listing
    })


@login_required
def watchlist(request):
    return None

@login_required
def add_comment(request):
    return None

@login_required
def categories(request):
    return None

@login_required
def place_bid(request):
    return None