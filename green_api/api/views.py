import requests
from rest_framework import viewsets, status
from rest_framework.response import Response
from .serializers import (
    CredentialsSerializer,
    SendMessageSerializer,
    SendFileSerializer
)

class GreenAPIViewSet(viewsets.ViewSet):
    def get_settings(self, request):
        serializer = CredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        url = f"https://api.green-api.com/waInstance{data['idInstance']}/getSettings/{data['apiTokenInstance']}"
        response = requests.get(url)
        return Response(response.json(), status=response.status_code)

    def get_state(self, request):
        serializer = CredentialsSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        url = f"https://api.green-api.com/waInstance{data['idInstance']}/getStateInstance/{data['apiTokenInstance']}"
        response = requests.get(url)
        return Response(response.json(), status=response.status_code)

    def send_message(self, request):
        serializer = SendMessageSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        url = f"https://api.green-api.com/waInstance{data['idInstance']}/sendMessage/{data['apiTokenInstance']}"
        payload = {
            "chatId": data["chatId"],
            "message": data["message"]
        }
        response = requests.post(url, json=payload)
        return Response(response.json(), status=response.status_code)

    def send_file(self, request):
        serializer = SendFileSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        url = f"https://api.green-api.com/waInstance{data['idInstance']}/sendFileByUrl/{data['apiTokenInstance']}"
        payload = {
            "chatId": data["chatId"],
            "urlFile": data["urlFile"],
            "fileName": data["fileName"]
        }
        response = requests.post(url, json=payload)
        return Response(response.json(), status=response.status_code)
