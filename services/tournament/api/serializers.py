from rest_framework import serializers
from .models import Tournament, User, Match, PlayerMatch, PlayerTournament
from django.db.models import Q
from .enums import *

class TournamentSerializer(serializers.ModelSerializer):
	class Meta:
		model = Tournament
		fields = ('id', 'name', 'status', 'round')

