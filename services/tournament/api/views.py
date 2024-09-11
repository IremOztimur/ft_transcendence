from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .enums import *
from .models import Tournament, User
from .serializers import TournamentSerializer


class TournamentView(APIView):
    def get(self, request):
        # Get Player Data
        user_id = request.user.id

        tournaments = Tournament.objects.filter(status=StatusChoices.PENDING.value)
        if not tournaments.exists():
            return Response({"statusCode": 404, "message": "No Tournaments available"}, status=status.HTTP_404_NOT_FOUND)

        serializer = TournamentSerializer(tournaments, many=True)
        return Response({"statusCode": 200, "tournaments": serializer.data}, status=status.HTTP_200_OK)
