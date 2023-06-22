from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=800)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    img_url = models.URLField(null=True, blank=True)
    category = models.CharField(max_length=80)

    def __str__(self):
        return f"{self.title}"

class Bid(models.Model):
    amount = models.DecimalField(max_digits=12, decimal_places=6)

class Comment(models.Model):
    content = models.CharField(max_length=80)


