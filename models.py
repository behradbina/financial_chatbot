from django.db import models


class Qa(models.Model):
    user_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    
class Feedback(models.Model):
    user_id = models.CharField(max_length=255)
    question = models.TextField()
    answer = models.TextField(null=True, blank=True)
    feedback = models.TextField(default="3")
    created_at = models.DateTimeField(auto_now_add=True)

class AudioFile(models.Model):
    user = models.CharField(max_length=100, blank=True, null=True)
    audio = models.FileField(upload_to="audio/")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Audio uploaded by {self.user or 'Anonymous'} at {self.uploaded_at}"
