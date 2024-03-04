from django.db import models
import uuid
from django.utils.timesince import timesince 
# Create your models here.
from account.models import User
class Conversation(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    users=models.ManyToManyField(User,related_name='conversations')
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True)
    def modified_at_formatted(self):
        return timesince(self.modified_at)

class ConversationMessage(models.Model):
    id=models.UUIDField(primary_key=True,editable=False,default=uuid.uuid4)
    conversation=models.ForeignKey(Conversation,related_name='messages',on_delete=models.CASCADE)
    body=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    created_by=models.ForeignKey(User,related_name='sent_messages',on_delete=models.CASCADE)
    sent_to=models.ForeignKey(User,related_name='received_messages',on_delete=models.CASCADE)
    def created_at_formatted(self):
        return timesince(self.created_at)