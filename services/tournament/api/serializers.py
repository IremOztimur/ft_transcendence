from rest_framework import serializers
from .models import Tournament, User, Match, PlayerMatch, PlayerTournament
from django.db.models import Q
from .enums import *

class PlayerSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ('id', 'avatar', 'alias_name')

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ('id', 'name', 'status', 'round')

	def is_player_in_tournament(self, player_id):
		tournament = Tournament.objects.filter(
			Q(playertournament__player=player_id) &
			(Q(status=StatusChoices.PENDING.value) |
			Q(status=StatusChoices.IN_PROGRESS.value))
		).first()
		return tournament

	def get_players(self, tournament):
		players_tournament = PlayerTournament.objects.filter(tournament=tournament)
		players = []
		for player_tournament in players_tournament:
			players.append(User.objects.get(id=player_tournament.player.id))
		player_data = PlayerSerializer(instance=players, many=True)
		return player_data.data

