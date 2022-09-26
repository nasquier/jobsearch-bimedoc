from rest_framework import serializers
from .models import HealthCareWorker


class HealthCareWorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthCareWorker
        fields = [
            "rpps_number",
            "last_name",
            "first_name",
            "profession_name",
        ]
