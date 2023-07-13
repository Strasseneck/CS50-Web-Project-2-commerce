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
        seller = request.user

        # Save listing
        listing = Listing(title=title,description=description,img_url=img,starting_bid=starting_bid,category=category,seller=seller)
        listing.save()
        return HttpResponseRedirect(reverse("index"))

def listing(request, title):
    current_user = request.user.id
    if not request.user.is_authenticated:
        listing = Listing.objects.get(title=title)
        return render(request, "auctions/listing.html", {
            "listing": listing
            })
    else:
        listing = Listing.objects.get(title=title)
        count = Watchlist.objects.filter(owner=current_user).count()
        watchlist = Watchlist.objects.filter(owner=current_user, item=listing)
        current_user = request.user.id
        if current_user == listing.seller.id:
            seller = 'Yes'
        else:
            seller = 'No'
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watchlist": watchlist,
            "count": count,
            "seller": seller,
            "current_user": current_user
        })
        
@login_required
def add_watchlist(request):
    if request.method == "POST":
        
        # Get data from form
        title = request.POST['title']
        listing = Listing.objects.get(title=title) 
        item = listing
        owner = request.user
        watchlist = Watchlist(owner=owner, item=item)

        # Save watchlist item
        watchlist.save()
        return HttpResponseRedirect(reverse("listing", args=(title,)))

@login_required
def remove_watchlist(request):
    if request.method == "POST":
        current_user = request.user
        title = request.POST['title']
        listing = Listing.objects.get(title=title) 
        watchlist = Watchlist.objects.filter(owner=current_user, item=listing)    

        # Delete watchlist item
        watchlist.delete()
        return HttpResponseRedirect(reverse("listing", args=(title,)))

@login_required
def watchlist(request):
    listings = []
    current_user = request.user
    watchlist = Watchlist.objects.filter(owner=current_user)
    for i in range(len(watchlist)):
        listings.append(watchlist[i].item)  
    return render(request, "auctions/watchlist.html", {
        "listings": listings
    })

@login_required
def place_bid(request):
        if request.method == "POST":
            title = request.POST['title']
            bidder = request.user

            # check bid is higher than starting price
            listing = Listing.objects.get(title=title)
            starting_price = listing.starting_bid
            bid = float(request.POST['bid'])
            if starting_price > bid:
                return HttpResponse("Your bid must be greater than or equal to the starting bid!")
            else:

                # check bid is higher than current bid
                current_price = float(listing.current_bid.amount)     
                if current_price == None:
                   
                    # save bid
                    new_bid = Bid(amount=bid, bidder=bidder)
                    new_bid.save()
                    listing.current_bid = new_bid
                    listing.save()
                    return HttpResponseRedirect(reverse("listing", args=(title,)))
                else:
                    if current_price >= bid:
                        return HttpResponse("Your bid must be higher than then the current highest bid")
                    else:
                        
                        # save bid
                        new_bid = Bid(amount=bid, bidder=bidder)
                        new_bid.save()
                        listing.current_bid = new_bid
                        listing.save()
                        return HttpResponseRedirect(reverse("listing", args=(title,)))
                    
@login_required
def close_listing(request):
    if request.method == "POST":
        # get title and listing object
        title = request.POST['title']
        listing = Listing.objects.get(title=title)
        winner = listing.current_bid.bidder
        print(winner)

        # edit and save listing
        listing.winner = winner
        listing.closed = True
        listing.save()
        return HttpResponseRedirect(reverse("listing", args=(title,)))


@login_required
def add_comment(request):
    return None

@login_required
def categories(request):
    return None

