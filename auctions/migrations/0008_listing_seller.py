# Generated by Django 4.2.2 on 2023-06-23 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_bid_bidder_comment_author_comment_time_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='seller',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
