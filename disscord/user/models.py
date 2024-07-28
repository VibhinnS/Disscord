from django.db import models
from disscord_servers.models import Server
from django.core.exceptions import ValidationError
from utils import search_trie
# Create your models here.


class User(models.Model):
    username = models.CharField(max_length=50, null=False, unique=True)
    account_created_on = models.DateTimeField(auto_now_add=True)
    date_of_birth = models.DateField()
    contact_number = models.CharField(max_length=10, blank=False, null=False)
    email_id = models.CharField(max_length=150, blank=False, null=False)


    def clean(self):
        username_lower = self.username.lower()
        for i in range(len(username_lower)):
            if search_trie.search(username_lower[i:]):
                return ValidationError("Can't keep this username")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

class ServerMembership(models.Model):
    roles = [
        ("MEMBER", "Member"),
        ("ADMIN", "Admin"),
        ("MODERATOR", "Moderator")
    ]
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    server = models.ForeignKey(Server, related_name='part_of_server', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    role = models.CharField(max_length=20, choices=roles, default="Member")

    class Meta:
        unique_together = ('user', 'server')