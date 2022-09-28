import requests
from django.http import JsonResponse
from django.db.models import Model
from rest_framework.serializers import Serializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import HealthCareWorker, Organization
from .serializers import HealthCareWorkerSerializer, OrganizationSerializer

directory_url = "https://6n1w6lwcmf.execute-api.eu-west-1.amazonaws.com/dev/"

# Cannot access CloudSearch schema without a token
# And CloudSearch crashes when one of the return fields asked is not in the schema
# So instead of directly extracting our models fields,
# we have to write the ones we know to be in the CloudSearch schema
response_fields = [
    "rpps_number",
    "last_name",
    "first_name",
    "profession_name",
    "finess",
    "registered_name",
]

# Utils
def get_worker_if_exists(rpps_number: str):
    try:
        worker = HealthCareWorker.objects.get(rpps_number=rpps_number)
    except HealthCareWorker.DoesNotExist:
        worker = None
    return worker


@api_view(["GET"])
def search_directory(request, search_term: str):
    if request.method != "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    response = requests.get(
        url=directory_url,
        params={
            "q": search_term,
            "return": ",".join(response_fields),
            "size": 10000,
        },
    )
    response_json = response.json()

    if response.status_code != 200 or "error" in response_json:
        return Response(
            response_json.get("error", None), status=status.HTTP_424_FAILED_DEPENDENCY
        )

    formatted_response = [worker["fields"] for worker in response_json["hits"]["hit"]]
    return JsonResponse(
        formatted_response,
        safe=False,
        json_dumps_params={"indent": 4, "ensure_ascii": False},
    )


@api_view(["POST"])
def save_worker(request):
    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    data = request.data
    rpps_number = data.get("rpps_number", None)
    worker = get_worker_if_exists(rpps_number)

    if data.get("finess", False):
        if worker:
            # Add finess from payload to worker's finess
            updated_list = worker.finess_list
            updated_list.append(data["finess"])
            worker.finess_list = list(set(updated_list))
        else:
            # Initialize finess list
            data["finess_list"] = [data["finess"]]

    # Update information with payload
    serializer = HealthCareWorkerSerializer(worker, data=data)

    if serializer.is_valid():
        serializer.save()
        save_organization_response = save_organization(request)
        message = (
            "Healt care worker and its organization have been added/updated successfully."
            if save_organization_response.status_code == status.HTTP_200_OK
            else "Health care worker added/updated, but organization missing or not recognized."
        )
        return Response(message, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def save_organization(request):
    if request.method != "POST":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    data = request.data
    finess = data.get("finess", None)

    try:
        organization = Organization.objects.get(finess=finess)
    except Organization.DoesNotExist:
        organization = None

    serializer = OrganizationSerializer(organization, data=data)

    if serializer.is_valid():
        serializer.save()
        return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
def list_workers(request):
    if request.method != "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    workers = HealthCareWorker.objects.all()
    sort_by_organization = {"NOT_REGISTERED": {"workers": []}}

    for worker in workers:
        serialized_worker = HealthCareWorkerSerializer(worker).data
        not_registered = True

        for finess in worker.finess_list:
            try:
                organization = Organization.objects.get(finess=finess)
            except Organization.DoesNotExist:
                continue

            not_registered = False

            if finess not in sort_by_organization:
                sort_by_organization[finess] = {
                    "organization_name": organization.registered_name,
                    "finess": finess,
                    "workers": [],
                }

            sort_by_organization[finess]["workers"].append(serialized_worker)

        if not_registered:
            sort_by_organization["NOT_REGISTERED"]["workers"].append(serialized_worker)

    return JsonResponse(
        sort_by_organization,
        safe=False,
        json_dumps_params={"indent": 4, "ensure_ascii": False},
    )


#  Classic REST CRUD for workers
@api_view(["GET"])
def healthcareworkers(request):
    if request.method != "GET":
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    workers = HealthCareWorker.objects.all()
    serializer = HealthCareWorkerSerializer(workers, many=True)

    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST", "GET", "PUT", "DELETE"])
def healthcareworker(request, rpps_number: str = None):
    worker = get_worker_if_exists(rpps_number=rpps_number)

    if request.method == "POST":
        if worker:
            return response_already_exists(worker)

        # Erase possible rpps_number in payload : we want the one in the url
        data = request.data
        data["rpps_number"] = rpps_number
        serializer = HealthCareWorkerSerializer(data=data)
        return save_if_valid_and_respond(serializer)

    if not worker:
        # GET PUT and DELETE must access an existing object to work
        return Response(status=status.HTTP_404_NOT_FOUND)

    serializer = HealthCareWorkerSerializer(worker)

    if request.method == "GET":
        return Response(serializer.data, status=status.HTTP_200_OK)

    if request.method == "PUT":
        payload_rpps_number = request.data.get("rpps_number", None)

        if payload_rpps_number and payload_rpps_number != worker.rpps_number:
            # If rpps_number is in payload, check if an existing object has it
            payload_target = get_worker_if_exists(payload_rpps_number)

            if payload_target:
                return response_already_exists(payload_target)

        serializer = HealthCareWorkerSerializer(worker, data=request.data)
        return save_if_valid_and_respond(serializer)

    if request.method == "DELETE":
        worker.delete()

        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)


# Global respond processes
def save_if_valid_and_respond(serializer: Serializer):
    # Check serializer validity. Save and return 200 if ok.
    # Else return 400
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_400_BAD_REQUEST)


def response_already_exists(model_object: Model):
    # Return 303 with the content of the existing object
    serializer = HealthCareWorkerSerializer(model_object)
    return Response(serializer.data, status=status.HTTP_303_SEE_OTHER)
