from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
   
class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=800)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=80)
    created = models.DateTimeField(auto_now=True)
    seller = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=6)
    bidder = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="bidders")

class Comment(models.Model):
    content = models.CharField(max_length=80)
    author = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="commenters")
    time = models.DateTimeField(auto_now=True)

class Seller (models.Model):
    name = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")

class Watchlist (models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="users")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="items")
