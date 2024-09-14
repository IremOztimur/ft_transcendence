from rest_framework import serializers
from .models import Tournament, Profil, Match, PlayerMatch, PlayerTournament
from django.db.models import Q
from .enums import *


class ProfilSerializer(serializers.ModelSerializer):
    #user = serializers.StringRelatedField(read_only=True)
    photo = serializers.ImageField(read_only=True)
    class Meta:
        model = Profil
        fields = ['user', 'photo', 'alias_name']

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
			players.append(Profil.objects.get(id=player_tournament.player.id))
		player_data = ProfilSerializer(instance=players, many=True)
		return player_data.data

	def get_player_number(self, tournament):
		players = PlayerTournament.objects.filter(tournament=tournament)
		return players.count()

	def get_creator(self, tournament):
		player = self.context.get("player")
		return PlayerTournament.objects.filter(tournament_id=tournament, player_id=player, creator=True).exists()
