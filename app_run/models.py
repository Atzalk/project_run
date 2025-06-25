from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class Run(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    athlete = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField()
    status = models.CharField(max_length=20,
                              choices=[('init', 'init'), ('in_progress', 'in_progress'), ('finished', 'finished')],
                              default='init')
