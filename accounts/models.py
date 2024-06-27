from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_teacher= models.BooleanField('Is teacher', default=False)
    is_student = models.BooleanField('Is student', default=False)

class PDFFile(models.Model):
    chapter_name = models.CharField(max_length=100)
    chapter_number = models.IntegerField()
    pdf_file = models.FileField(upload_to='pdfs/')
    uploadedBy = models.ForeignKey(User, on_delete=models.CASCADE, related_name="uploadedBy")
    subject = models.CharField(max_length=100,default = "EMBEDDED SYSTEMS")
    views_count = models.PositiveIntegerField(default=0)
    def __str__(self):
        return f'{self.chapter_name} - Chapter {self.chapter_number}'
    
class PDFView(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    pdf = models.ForeignKey(PDFFile, on_delete=models.CASCADE)
    viewed_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'pdf')
    
