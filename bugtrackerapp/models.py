from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    pass


class Ticket(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)
    description = models.CharField(max_length=250)
    filing_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='filing_user')

    NEW = 'New'
    IN_PROGRESS = 'In Progress'
    DONE = 'Done'
    INVALID = 'Invalid'

    TICKET_STATUS_CHOICES = [
        (NEW, 'New'),
        (IN_PROGRESS, 'In Progress'),
        (DONE, 'Done'),
        (INVALID, 'Invalid')
    ]
    ticket_status = models.CharField(max_length=25, choices=TICKET_STATUS_CHOICES, default=NEW)
    assigned_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='assigned_user', blank=True, null=True)
    completed_user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='completed_user', blank=True, null=True)

    def __str__(self):
        return self.title

    def url(self):
        return f"/ticket/{self.id}"