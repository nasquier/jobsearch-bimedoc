# Generated by Django 4.1.1 on 2022-09-27 07:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_directory", "0005_healthcareworker_id_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthcareworker",
            name="organizations",
            field=models.JSONField(blank=True, default=list),
        ),
    ]