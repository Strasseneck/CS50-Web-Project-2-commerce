# Generated by Django 4.2.2 on 2023-06-21 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0003_category_alter_listing_category'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Category',
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(max_length=80),
        ),
    ]
