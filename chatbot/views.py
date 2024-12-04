import os

from langchain.docstore.document import Document
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser
from django.http import JsonResponse, FileResponse, HttpResponse


from .language_prepro import PreproText
from .models import Qa, Feedback
from .retriever import Retriever
from .create_answer import CreateAnswer
from .serializers import QaSerializer, AddContextSerializer, SaveFeedbackSerializer, QaResponseSerializer, \
    AddContextResponseSerializer, SaveFeedbackResponseSerializer, AudioFileSerializer


qa_instance = CreateAnswer()
text_cleaner = PreproText()


class QaAPIView(APIView):
    @extend_schema(request=QaSerializer, responses=QaResponseSerializer)
    def post(self, request):
        serializer = QaSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        question = serializer.validated_data['question']
        user_id = serializer.validated_data['user_id']
        
        answer, status_flag = qa_instance.get_question(question, user_id)
        Qa.objects.create(user_id=user_id, question=question, answer=answer)
        
        return Response({'answer': answer}, 
            status=status.HTTP_201_CREATED if status_flag else status.HTTP_400_BAD_REQUEST
            )


class SaveFeedbackAPIView(APIView):
    @extend_schema(request=SaveFeedbackSerializer, responses=SaveFeedbackResponseSerializer)
    def post(self, request):
        serializer = SaveFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            Feedback.objects.create(**serializer.validated_data)
            return Response(status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)


class AddContextAPIView(APIView):
    @extend_schema(request=AddContextSerializer, responses=AddContextResponseSerializer)
    def post(self, request):
        serializer = AddContextSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        context = text_cleaner.clean_context(serializer.validated_data.get('context'))
        
        try:
            document = Document(page_content=context)
            retriever = Retriever()
            retriever.insert_new_data(document)
            return Response(status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class VoiceRecordAPI(APIView):
    parser_classes = [MultiPartParser]
    def post(self, request, *args, **kwargs):
        serializer = AudioFileSerializer(data=request.data)
        if serializer.is_valid():
            uploaded_voice = serializer.save()
            return Response({
                "message": "Voice file uploaded successfully.",
                "file_name": uploaded_voice.audio.name,
                "upload_time": uploaded_voice.uploaded_at,
            })
        return Response(serializer.errors, status=400)
    
    def get(self, request, *args, **kwargs):
        file_path = r"C:\Users\B_Binaei\Desktop\work\f_chatbot\test.wav" 
        if not file_path or not os.path.exists(file_path):
            return JsonResponse({"error": "File path is invalid or file does not exist."}, status=400)

        try:
            response = FileResponse(open(file_path, 'rb'), content_type='audio/wav')
            response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
            return response
        except Exception as e:
            return HttpResponse(f"Error playing audio: {str(e)}", status=500)
