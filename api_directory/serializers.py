from rest_framework import serializers
from .models import HealthCareWorker, Organization


class HealthCareWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCareWorker
        fields = [
            "rpps_number",
            "last_name",
            "first_name",
            "profession_name",
        ]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = [
            "finess",
            "name",
        ]
