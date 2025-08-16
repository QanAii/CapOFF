from django.core.serializers import serialize
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import UserRegisterSerializer


class UserRegisterView(APIView):

    def post(self, request):
        serializers = UserRegisterSerializer(data=request.data)

        if serializers.is_valid():
            serializers.save()
            return Response(serializers.data, status.HTTP_201_CREATED)
        return Response(status.HTTP_400_BAD_REQUEST)
