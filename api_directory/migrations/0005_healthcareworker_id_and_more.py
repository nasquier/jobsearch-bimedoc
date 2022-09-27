# Generated by Django 4.1.1 on 2022-09-26 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("api_directory", "0004_alter_healthcareworker_first_name_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="healthcareworker",
            name="id",
            field=models.BigAutoField(
                auto_created=True,
                default=None,
                primary_key=True,
                serialize=False,
                verbose_name="ID",
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="healthcareworker",
            name="rpps_number",
            field=models.CharField(max_length=100, unique=True),
        ),
    ]
