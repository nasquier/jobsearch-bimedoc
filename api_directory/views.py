from django.http import JsonResponse
from .models import HealthCareWorker
from .serializers import HealthCareWorkerSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.exceptions import ErrorDetail
from rest_framework import status


@api_view(["GET", "POST"])
def healthcareworkers(request):
    if request.method == "GET":
        workers = HealthCareWorker.objects.all()
        serializer = HealthCareWorkerSerializer(workers, many=True)
        return JsonResponse(serializer.data, safe=False)

    if request.method == "POST":
        serializer = HealthCareWorkerSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
