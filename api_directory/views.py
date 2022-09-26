from django.http import JsonResponse
from .models import HealthCareWorker
from .serializers import HealthCareWorkerSerializer


def healthcareworkers_list(request):
    workers = HealthCareWorker.objects.all()
    serializer = HealthCareWorkerSerializer(workers, many=True)
    return JsonResponse(serializer.data)