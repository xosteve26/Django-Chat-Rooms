from django.db import models

# Create your models here.
class Room(models.Model):
    #host
    #topic
    name=models.CharField(max_length=255)
    description=models.TextField(null=True, blank=True)
    #participants=
    updated=models.DateTimeField(auto_now=True)
    created=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Message(models.Model):
    #user=
    room=models.ForeignKey(Room, on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def _str_ (self):
        return self.body[:50]