from django.contrib import admin
from .models import HealthCareWorker, Organization

admin.site.register(HealthCareWorker)
admin.site.register(Organization)
