from django.db import models

# Create your models here.
class Content(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey("auth.user", models.CASCADE)
    title = models.CharField(max_length=200)
    transcription = models.TextField()
    created = models.DateTimeField(auto_now_add=True)