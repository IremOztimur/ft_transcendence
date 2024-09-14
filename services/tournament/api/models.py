from django.db import models
from .enums import State, Status, StatusChoices
from django.contrib.auth.models import User

from django.contrib.auth.models import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email=None, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if email:
            email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class Profil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profil')
    bio = models.CharField(max_length=300, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    photo = models.ImageField(blank=True, null=True, upload_to='profil_photo/%Y/%m/')
    two_factory = models.BooleanField(default=False)
    otp_secret_key = models.CharField(max_length=64, blank=True, null=True)
    STATUS_CHOICES = [
        (Status.ONLINE.value, 'ONLINE'),
        (Status.OFFLINE.value, 'OFFLINE'),
        (Status.INGAME.value, 'INGAME')
	]
    alias_name = models.CharField(max_length=100, null=True, blank=True)
    wins = models.IntegerField(default=0, blank=False, null=False)
    losses = models.IntegerField(default=0, blank=False, null=False)
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default=Status.OFFLINE.value)
    championships = models.IntegerField(default=0, blank=False, null=False)

class PlayerMatch(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=False, blank=False)
    player = models.ForeignKey(Profil, on_delete=models.CASCADE, null=False, blank=False)
    score = models.IntegerField(default=0, null=False, blank=False)
    won = models.BooleanField(default=False, null=False, blank=False)

    def __str__(self):
        return f"Score: {self.score}"


class Match(models.Model):
    id = models.AutoField(primary_key=True)
    tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=True, blank=False)
    round = models.IntegerField(default=1)
    state = models.CharField(max_length=3, choices=State.choices(), null=False, blank=False, default=State.UNPLAYED.value)

    def __str__(self):
        return f"Match Round: {self.round}"

class PlayerTournament(models.Model):
	id = models.AutoField(primary_key=True)
	tournament = models.ForeignKey('Tournament', on_delete=models.CASCADE, null=False, blank=False)
	player = models.ForeignKey(Profil, on_delete=models.CASCADE, null=False, blank=False)
	creator = models.BooleanField(default=False, null=False, blank=False)

	def __str__(self):
		return f'{self.player_id} -> {self.creator}'

class Tournament(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=30, null=False, blank=False, unique=False)
	round = models.IntegerField(default=1)
	status = models.CharField(max_length=2,
						choices=StatusChoices.choices(),
						default=StatusChoices.PENDING.value,
						null=False,
						blank=False)

	def __str__(self):
		return f"Tournament ID: {self.id}"
