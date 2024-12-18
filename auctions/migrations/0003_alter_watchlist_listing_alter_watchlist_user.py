# Generated by Django 5.0.6 on 2024-11-06 14:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0002_alter_bids_options_alter_comments_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="watchlist",
            name="listing",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watchlist",
                to="auctions.listings",
            ),
        ),
        migrations.AlterField(
            model_name="watchlist",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="watched_by",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
