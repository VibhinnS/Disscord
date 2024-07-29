from rest_framework import serializers
from disscord_servers.models import Server

class DisscordServerSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model=Server
        fields='__all__'