# Generated by Django 4.1.5 on 2023-02-06 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api", "0002_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="announcements",
            name="views",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="morningdevotion",
            name="views",
            field=models.IntegerField(default=0),
        ),
    ]