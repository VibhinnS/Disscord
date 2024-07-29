from rest_framework import viewsets
from disscord_servers.models import Server
from disscord_servers.serializers import DisscordServerSerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all()
    serializer_class = DisscordServerSerializer

