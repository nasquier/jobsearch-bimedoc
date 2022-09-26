from django.db import models


class HealthCareWorker(models.Model):
    rpps_number = models.CharField(max_length=100, primary_key=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    first_name = models.CharField(max_length=100, default="", blank=True)
    profession_name = models.CharField(max_length=100, default="", blank=True)
