from django.db import models


class HealthCareWorker(models.Model):
    rpps_number = models.CharField(max_length=100, unique=True)
    last_name = models.CharField(max_length=100, default="", blank=True)
    first_name = models.CharField(max_length=100, default="", blank=True)
    profession_name = models.CharField(max_length=100, default="", blank=True)
    finess_list = models.JSONField(default=list, blank=True)

    def __str__(self):
        return f"{self.rpps_number} - {self.last_name.upper()} {self.first_name}, {self.profession_name}"


class Organization(models.Model):
    finess = models.CharField(max_length=100, unique=True)
    registered_name = models.CharField(max_length=100, default="", blank=True)

    def __str__(self):
        return f"{self.finess} - {self.registered_name}"
