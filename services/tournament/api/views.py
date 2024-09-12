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
		name = request.data.get('tournament_name')
		alias = request.data.get('alias_name')

		try:
			player = User.objects.get(id=user_id)
		except User.DoesNotExist:
			return Response({"statusCode": 400, "message": "Player does not exist"})

		if action == 'create':
			if (name is None or alias is None or len(alias) == 0):
				return Response({"statusCode": 400, "message": "Invalid Tournament Request"}, status=status.HTTP_400_BAD_REQUEST)
			serializer = TournamentSerializer()
			if serializer.is_player_in_tournament(player.id):
				return Response({"statusCode": 400, "message": "Player already in a tournament"}, status=status.HTTP_400_BAD_REQUEST)
			tournament = Tournament.objects.create(name=name)
			PlayerTournament.objects.create(player=player, tournament=tournament, creator=True)
			serializer = TournamentSerializer(tournament)
			player.alias_name = alias
			player.save()
			return Response({"statusCode": 200,
					 "message": "Tournament created successfully",
					 "current_tournament": serializer.get_players(tournament)}, status=201)

		return Response({"statusCode": 200, "message": "Tournament created successfully"}, status=status.HTTP_200_OK)
