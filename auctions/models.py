from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Bid(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="bidders")

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=800)
    starting_bid = models.DecimalField(null=True, max_digits=10, decimal_places=2)
    current_bid = models.ForeignKey(Bid, null=True, blank=True, on_delete=models.CASCADE, related_name="bids")
    img_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    winner = models.ForeignKey(User, null=True, blank=True, on_delete=models.CASCADE, related_name="winners")
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"

class Comment(models.Model):
    listing = models.ForeignKey(Listing, null=True, on_delete=models.CASCADE, related_name="commented_listings")
    content = models.CharField(max_length=80)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="commenters")
    time = models.DateTimeField(auto_now=True)

class Seller (models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")

class Watchlist (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
