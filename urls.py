from django.urls import path
from .views import QaAPIView, AddContextAPIView, SaveFeedbackAPIView, VoiceRecordAPI


urlpatterns = [
    path('chatbot/', QaAPIView.as_view()),
    path('add-context/', AddContextAPIView.as_view()),
    path('feedback/', SaveFeedbackAPIView.as_view()),
    path("voice-record/", VoiceRecordAPI.as_view(), name="voice-record"),
]
