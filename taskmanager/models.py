from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Board(models.Model):
    name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return self.name
    
class Column(models.Model):
    name = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.name
    
class Card(models.Model):
    name = models.CharField(max_length=100)
    content= models.TextField()
    date= models.DateTimeField(auto_now_add=True)
    column = models.ForeignKey(Column, on_delete=models.CASCADE)

    def __str__(self):
        return self.name