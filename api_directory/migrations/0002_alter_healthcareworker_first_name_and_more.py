# Generated by Django 4.1.1 on 2022-09-26 19:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_directory", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="healthcareworker",
            name="first_name",
            field=models.CharField(default="", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="healthcareworker",
            name="last_name",
            field=models.CharField(default="", max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="healthcareworker",
            name="profession_name",
            field=models.CharField(default="", max_length=100, null=True),
        ),
    ]
