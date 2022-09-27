from django.db import models


class HealthCareWorker(models.Model):
    rpps_number = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    first_name = models.CharField(max_length=100, default="", blank=True)
    profession_name = models.CharField(max_length=100, default="", blank=True)
    organizations_finess = models.JSONField(default=list, blank=True)
