# Generated by Django 4.1.1 on 2023-08-28 11:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("blog", "0002_blogindexpage"),
    ]

    operations = [
        migrations.RenameField(
            model_name="blogpage",
            old_name="blog_image",
            new_name="image",
        ),
    ]
