from django.db import models
from django.contrib.auth.models import User

class Document(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    pdf = models.FileField(upload_to='pdf')

    def __str__(self):
        return self.name
    
class Quiz(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    quiz_name = models.CharField(max_length=255, blank=True, null=True)
    attempt_number = models.IntegerField(default=1)
    question = models.TextField()
    correct_answer = models.TextField()
    user_answer = models.TextField()
    correct = models.BooleanField(default=False)

    def __str__(self):
        return self.quiz_name + "\n" + str(self.attempt_number)