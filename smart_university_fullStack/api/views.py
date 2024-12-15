from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from data_collect.models import ControlSettingsRecive
from .serializers import ControlSettingsPublishSerializer,ControlSettingsReciveSerializer

class ControlSettingsView(APIView):
    def get(self, request):
        try:
            control_settings = ControlSettingsRecive.objects.first()
            serializer = ControlSettingsReciveSerializer(control_settings)
            return Response(serializer.data)
        except ControlSettingsRecive.DoesNotExist:
            return Response({"error": "ControlSettings1 does not exist"}, status=status.HTTP_404_NOT_FOUND)
    def post(self, request):
            serializer = ControlSettingsPublishSerializer(data=request.data)
            
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            print('this is the body of the request -----',request.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
   