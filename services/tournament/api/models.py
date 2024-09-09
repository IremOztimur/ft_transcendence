from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .enums import Round, State, Status, StatusChoices

class User(AbstractBaseUser):
	STATUS_CHOICES = [
		(Status.ONLINE.value, 'ONLINE'),
		(Status.OFFLINE.value, 'OFFLINE'),
		(Status.INGAME.value, 'INGAME')
	]

	id = models.AutoField(primary_key=True)
	username = models.CharField(max_length=20, blank=False, null=False, unique=False)
	email = models.EmailField(max_length=30, blank=False, null=False, unique=True)
	alias_name = models.CharField(max_length=100, unique=True, null=False, blank=False)
	wins = models.IntegerField(default=0, blank=False, null=False)
	losses = models.IntegerField(default=0, blank=False, null=False)
	status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=Status.OFFLINE.value)
	championships = models.IntegerField(default=0, blank=False, null=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['email']

	def __str__(self):
		return f'Player: [ alias: {self.alias_name}, username: {self.username} ]'


class PlayerMatch(models.Model):
    id = models.AutoField(primary_key=True)
    match_id = models.ForeignKey('Match', on_delete=models.CASCADE, null=False, blank=False)
    player_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    score = models.IntegerField(default=0, null=False, blank=False)
    won = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return f"Score: {self.score}"


class Match(models.Model):

    id = models.AutoField(primary_key=True)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=False)
    round = models.CharField(max_length=2, choices=Round.choices(), null=False, blank=False)
    state = models.CharField(max_length=3, choices=State.choices(), null=False, blank=False, default=State.UNPLAYED.value)

    def __str__(self):
        return f"Match Round: {self.round}"

class PlayerTournament(models.Model):
	id = models.AutoField(primary_key=True)
	tournament_id = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=False, blank=False)
	player_id = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
	creator = models.BooleanField(default=False, null=False, blank=False)

	def __str__(self):
		return f'{self.player_id} -> {self.creator}'

class Tournament(models.Model):


	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, null=False, blank=False, unique=False)
	round = models.CharField(max_length=2, choices=Round.choices(), null=False, blank=False)
	status = models.CharField(max_length=2,
						choices=StatusChoices.choices(),
						default=StatusChoices.PENDING.value,
						null=False,
						blank=False)

	def __str__(self):
		return f"Tournament ID: {self.id}"
