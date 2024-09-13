from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .enums import *
from .models import Tournament, User, PlayerTournament
from .serializers import TournamentSerializer
from django.contrib.auth import get_user_model

User = get_user_model()

class TournamentView(APIView):
	def get(self, request):
		# Get Player Data
		user_id = request.user.id
		player = User.objects.get(id=user_id)

		# Handle case where no tournament is available
		tournaments = Tournament.objects.filter(status=StatusChoices.PENDING.value)
		if not tournaments.exists():
			return Response({"statusCode": 404, "message": "No Tournaments available"}, status=status.HTTP_404_NOT_FOUND)

		serializer = TournamentSerializer(tournaments, many=True)
		return Response({"statusCode": 200, "tournaments": serializer.data}, status=status.HTTP_200_OK)

	def post(self, request):
		action = request.data.get('action')
		user_id = request.user.id

		try:
			player = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return Response({"statusCode": 400, "message": "Player does not exist"})

		if action == 'create':
			return self.create_tournament(request, player)

	def create_tournament(self, request, player):
		name = request.data.get('tournament_name')
		alias = request.data.get('alias_name')

		if not name or not alias:
			return Response({"statusCode": 400, "message": "Invalid Tournament name or alias"})

		serializer = TournamentSerializer()
		if serializer.is_player_in_tournament(player.id):
			return Response({"statusCode": 400, "message": "Player already in a tournament"}, status=status.HTTP_400_BAD_REQUEST)

		tournament = Tournament.objects.create(name=name)
		PlayerTournament.objects.create(player=player, tournament=tournament, creator=True)

		player.alias_name = alias
		player.save()

		serializer = TournamentSerializer(tournament)
		return Response({
			"statusCode": 201,
			"message": "Tournament created successfully",
			"current_tournament": serializer.get_players(tournament)
			}, status=201)
