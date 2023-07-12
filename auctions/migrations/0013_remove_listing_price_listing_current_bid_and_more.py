# Generated by Django 4.2.2 on 2023-07-12 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_watchlist_item'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='price',
        ),
        migrations.AddField(
            model_name='listing',
            name='current_bid',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True),
        ),
        migrations.AddField(
            model_name='listing',
            name='starting_bid',
            field=models.DecimalField(decimal_places=2, max_digits=10, null=True),
        ),
    ]
