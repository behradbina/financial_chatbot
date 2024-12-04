from rest_framework import serializers
from .models import Qa, Feedback, AudioFile

class QaSerializer(serializers.ModelSerializer):    
    class Meta:
        model = Qa
        fields = ['user_id', 'question']

class AddContextSerializer(serializers.Serializer):
    context = serializers.CharField(max_length=512)
    
class SaveFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['user_id', 'question', 'answer', 'feedback']

class AudioFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioFile
        fields = '__all__'

"""
Serializers for Swagger  Response
"""
class QaResponseSerializer(serializers.Serializer):
    answer = serializers.CharField(max_length=1024)
    responseCode = serializers.IntegerField()
    responseDesc = serializers.CharField(max_length=255)


class AddContextResponseSerializer(serializers.Serializer):
    context = serializers.CharField(max_length=512)


class SaveFeedbackResponseSerializer(serializers.Serializer):
    responseCode = serializers.IntegerField()
    responseDesc = serializers.CharField(max_length=255)
