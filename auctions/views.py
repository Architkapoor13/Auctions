from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django import forms
from django.contrib.auth.decorators import login_required

from .models import *


class NewListingForm(forms.Form):
    title = forms.CharField(label="Title", widget = forms.TextInput(attrs={'class': "form-control", 'id': "exampleFormControlSelect1"}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': "form-control", 'id': "exampleFormControlTextarea1"}))
    Choices = (('Toys','Toys'), ('Books','Books'), ('Musicals','Musicals'), ('Home','Home'), ('Electronics', 'Electronics'), ('Fashion', 'Fashion'), ('Computer','Computer'))
    category = forms.ChoiceField(widget = forms.Select(attrs={'class': "custom-select", 'id': "inputGroupSelect01"}), choices=Choices)
    starting_bid = forms.FloatField(label="Starting Bid", widget= forms.TextInput(attrs={'class': 'form-control col-3'}))
    piclink = forms.CharField(max_length=200, label="Picture Link", widget=forms.TextInput(attrs={'class': "form-control col-4"}), required=False)

def index(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.filter(isactive=True)
    })

def alllistings(request):
    return render(request, "auctions/index.html", {
        "listings": AuctionListing.objects.all(),
        "flag": 1
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

def newlisting(request):
    if request.method == "POST":
        form = NewListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            description = form.cleaned_data["description"]
            category = form.cleaned_data["category"]
            sbid = form.cleaned_data["starting_bid"]
            piclink = form.cleaned_data["piclink"]
            if piclink == "":
                piclink = "https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRqEWgS0uxxEYJ0PsOb2OgwyWvC0Gjp8NUdPw&usqp=CAU"
            AuctionListing.objects.create(
                user = request.user,
                title = title,
                description = description,
                category = category,
                startingbid = sbid,
                currentbid = sbid,
                piclink = piclink
            )
            print("form working!")
            return HttpResponseRedirect(reverse("index"))
    return render(request, "auctions/nlisting.html", {
        "form": NewListingForm()
    })


def listing(request, listing_code):
    auclisting = AuctionListing.objects.get(pk=listing_code)
    comments = Comments.objects.filter(item = auclisting)
    comcount = comments.count()
    if not request.user.is_authenticated:
        global watchcount
        watchcount = 0
    else:
        watchlistlistings = Watchlist.objects.filter(user= request.user, item=auclisting)
        watchcount = watchlistlistings.count()
    if request.method == 'POST':
        newbid = request.POST['bid']
        dblistings = AuctionListing.objects.get(pk = listing_code)
        if float(newbid) > dblistings.currentbid:
            Bids.objects.create(
                user = request.user,
                item = dblistings,
                bid = float(newbid)
            )
            print("new bid listing created")
            dblistings.currentbid = newbid
            dblistings.save()
            message = "Bid Placed!"
            bid = Bids.objects.filter(item = dblistings)
            count = bid.count()
            global latestbid
            if count == 0:
                latestbid = None
            else:
                latestbid = bid[count - 1].user
            return render(request, "auctions/listings.html", {
                "listing": dblistings,
                "placedmessage": message,
                "count": count,
                "latestbidder": latestbid,
                "comments": comments,
                "comcount": comcount,
                "watchcount": watchcount
            })
        else:
            bid = Bids.objects.filter(item=dblistings)
            count = bid.count()
            global latestbids
            if count == 0:
                latestbids = None
            else:
                latestbids = bid[count - 1].user
            message = "Sorry, the bid you placed is less than the current price."
            return render(request, "auctions/listings.html", {
                "listing": dblistings,
                "errormessage": message,
                "count": count,
                "latestbidder": latestbids,
                "comments": comments,
                "comcount": comcount,
                "watchcount": watchcount
            })


    bids = Bids.objects.filter(item=auclisting)
    print(bids)
    count = bids.count()
    global latestbidder
    if count == 0:
        latestbidder = None
    else:
        latestbidder = bids[count-1].user
    return render(request, "auctions/listings.html",{
        "listing": auclisting,
        "count": count,
        "latestbidder": latestbidder,
        "comments": comments,
        "comcount": comcount,
        "watchcount": watchcount
    })
@login_required
def userwatchlist(request):
    if request.method == "POST":
        id = request.POST['watchlistid']
        auclisting = AuctionListing.objects.get(id = id)
        watchlisting = Watchlist.objects.filter(user=request.user, item=auclisting)
        print(watchlisting)
        if watchlisting.count() == 0:
            Watchlist.objects.create(
                user = request.user,
                item = auclisting
            )
            print("item added to watchlist")
        else:
            watchlisting.delete()
            print("item removed from the watchlist")
        return redirect(f"/listings/{id}")
    watchlisting = Watchlist.objects.filter(user=request.user)
    return render(request, "auctions/watchlist.html",{
        "listings": watchlisting
    })

def close(request):
    id = request.POST['closing']
    lisitng = AuctionListing.objects.get(pk = id)
    lisitng.isactive = False
    lisitng.save()
    return redirect(f"/listings/{id}")

def isclosedmsg(request, listing_code):
    closingmsg = "No more bids allowed as this bid closed now!"
    listing = AuctionListing.objects.get(pk = listing_code)
    bids = Bids.objects.filter(item = listing)
    count = bids.count()
    watchlistlistings = Watchlist.objects.filter(user=request.user, item=listing)
    watchcount = watchlistlistings.count()
    global latestbidder
    if count == 0:
        latestbidder = None
    else:
        latestbidder = bids[count-1].user
    comments = Comments.objects.filter(item=listing)
    comcount = comments.count()
    return render(request, "auctions/listings.html", {
        "listing": listing,
        "count": count,
        "latestbidder": latestbidder,
        "comments": comments,
        "comcount": comcount,
        "closingmsg": closingmsg,
        "watchcount": watchcount
    })

def comments(request):
    if request.method == "POST":
        comment = request.POST['comment']
        id = request.POST['commentlisting']
        listing = AuctionListing.objects.get(pk = id)
        Comments.objects.create(
            user = request.user,
            item = listing,
            comment = comment
        )
        print("comment added")
        return redirect(f"/listings/{id}")

cat = ["Toys", "Musicals", "Home", "Electronics", "Computer", "Fashion"]

def categories(request):
    return render(request, "auctions/categories.html", {
        "categories": cat
    })

def category(request, cat):
    auclistings = AuctionListing.objects.filter(category=cat, isactive=True)
    return render(request, "auctions/index.html", {
        "listings": auclistings,
        "category": cat,
        "flag": 2
    })

@login_required
def mylistings(request):
    listings = AuctionListing.objects.filter(user=request.user)
    return render(request, "auctions/index.html", {
        "listings": listings,
        "flag": 3
    })

