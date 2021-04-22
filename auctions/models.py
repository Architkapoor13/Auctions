from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_auctions", null=True)
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=500)
    category = models.CharField(max_length=64)
    startingbid = models.FloatField()
    piclink = models.CharField(max_length=200, default="https://encrypted-tbn0.gstatic.com/images?q=tbn%3AANd9GcRqEWgS0uxxEYJ0PsOb2OgwyWvC0Gjp8NUdPw&usqp=CAU")
    currentbid = models.FloatField()
    isactive = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Title: {self.title} " \
               f"Catrgory: {self.category} " \
               f"Starting bid: {self.startingbid} " \
               f"Created by - {self.user.username}"

class Bids(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids_by_user")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bid_on_title")
    bid = models.FloatField()

    def __str__(self):
        return f"Bid: {self.bid} on {self.item} by {self.user}"

class Comments(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments_by_user")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments_on_title")
    comment = models.CharField(max_length=200)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"comment: {self.comment} by {self.user}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist_of_user")
    item = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="item_in_watchlist")

    def __str__(self):
        return f"watchlist owener: {self.user} containg {self.item}"

