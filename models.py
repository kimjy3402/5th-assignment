from django.db import models
from django.utils import timezone


# Create your models here.


class Blog(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()

    def __str__(self):
        return self.title
        
    
    # objects = models.Manager()

    def summary(self):
        return self.body[:100] #pylint: disable=E1136

class Comment(models.Model):
    post = models.ForeignKey('Blog', on_delete=models.CASCADE, related_name='comments')
    # author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    # approved_comment = models.BooleanField(default=False)

    # def approve(self):
    #     self.approved_comment = True
    #     self.save()

    def __str__(self):
        return self.text