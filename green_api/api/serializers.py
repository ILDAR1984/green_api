from rest_framework import serializers

class CredentialsSerializer(serializers.Serializer):
    idInstance = serializers.CharField()
    apiTokenInstance = serializers.CharField()

class SendMessageSerializer(CredentialsSerializer):
    chatId = serializers.CharField()
    message = serializers.CharField()

class SendFileSerializer(CredentialsSerializer):
    chatId = serializers.CharField()
    urlFile = serializers.URLField()
    fileName = serializers.CharField()
