import pytest
from django.test import TestCase
from django.contrib.auth.models import User
from .models import Server
from django.core.exceptions import ValidationError

class ServerModelTests(TestCase):
        # Creating a server with valid name and type
    def test_create_server_with_valid_name_and_type(self):
        user = User.objects.create(username='testuser')
        server = Server.objects.create(server_name='TestServer', server_type='PUBLIC', owner=user)
        assert server.server_name == 'TestServer'
        assert server.server_type == 'PUBLIC'
        assert server.owner == user
    
    # Attempt to save a server with an empty name
    def test_save_server_with_empty_name(self):
        server = Server(server_name="")
        with pytest.raises(ValidationError, match="Server can't be nameless aneki!"):
            server.save()    

    def test_associate_server_with_owner(self):
        user = User.objects.create(username='testuser')
        server = Server.objects.create(server_name='TestServer', server_type='PUBLIC', owner=user)
        assert server.server_name == 'TestServer'
        assert server.server_type == 'PUBLIC'
        assert server.owner == user

        # Retrieving servers owned by a specific user
    def test_retrieve_servers_owned_by_specific_user(self):
        user = User.objects.create(username='testuser')
        server = Server.objects.create(server_name='TestServer', server_type='PUBLIC', owner=user)
        retrieved_servers = Server.objects.filter(owner=user)
        assert server in retrieved_servers

    def test_create_server_with_name_exceeding_max_length(self):
        user = User.objects.create(username='testuser')
        long_name = 'A' * 26
        server = Server(server_name=long_name, server_type='PUBLIC', owner=user)
        
        with self.assertRaises(ValidationError):
            server.full_clean()
            server.save()
