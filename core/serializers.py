from rest_framework import serializers
from core.models import UploadImage, Log


class UploadImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = UploadImage
        fields = ['img']


class LogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Log
        fields = ['masked_user', 'un_masked_user', 'created_at']
