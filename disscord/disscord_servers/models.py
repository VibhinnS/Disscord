from django.db import models
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from user.models import User

#disscord Server data model
class Server(models.Model):
    SERVER_OPTION = [
        ("PUBLIC", "Public"),
        ("PRIVATE", "Private")
    ]
    
    server_name = models.CharField(max_length=25, null=False)
    server_type = models.CharField(max_length=7, choices=SERVER_OPTION)
    created_at = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='owned_servers', null=True)

    def clean(self):
        if not self.server_name.strip():
            raise ValidationError("Server can't be nameless aneki!")
        if len(self.server_name.strip()) > 25:
            raise ValidationError("Length can't be more than 25 characters!")

    def save(self, *args, **kwargs):
        self.full_clean() 
        super().save(*args, **kwargs)

    def __str__(self):
        return self.server_name


#channel data model - each server may have multiple channels
class Channel(models.Model):
    CHANNEL_TYPE = [
        ("TEXT", "Text"),
        ("VOICE", "Voice")
    ]
    server = models.ForeignKey(Server, related_name='channels', on_delete=models.CASCADE)
    channel_name = models.CharField(max_length=50, null=False)
    channel_type = models.CharField(max_length=5, choices=CHANNEL_TYPE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'#{self.channel_name} - {self.server}'


class Message(models.Model):
    channel = models.ForeignKey(Channel, related_name='messages_posted', on_delete=models.CASCADE)
    sender = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to='attachments/')
    message_sent_at = models.DateTimeField(auto_now_add=True)
    message_edited_at = models.DateTimeField(blank = True, null=True)

    def __str__(self):
        return f'{self.content} in #{self.channel} - {self.channel.server}'

    
class Invite(models.Model):
    PERMANENT = 'PERM'
    NORMAL = 'TEMP'
    INVITE_TYPE = [
        (PERMANENT, "Permanent"),
        (NORMAL, "Temporary")
    ]
    server = models.ForeignKey(Server, on_delete=models.CASCADE, related_name='server_invites')
    unique_code = models.CharField(max_length=10, null=True, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    type = models.CharField(max_length=4, choices=INVITE_TYPE)
    created_by = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if self.type == self.PERMANENT:
            self.expires_at = None
        if self.type == self.NORMAL:
            self.expires_at = timezone.now() + timedelta(days = 3)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.created_by} invites you to join Disscord @{self.server} - link expires in {self.expires_at}!"
