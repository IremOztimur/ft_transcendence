from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from .enums import State, Status, StatusChoices
from PIL import Image

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
	avatar = models.ImageField(blank=True, null=True, upload_to='profil_photo/%Y/%m/')

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['alias_name']

	objects = CustomUserManager()

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.avatar:
			img = Image.open(self.avatar.path)
			if img.height > 600 or img.width > 600:
				output_size = (600,600)
				img.thumbnail(output_size)
				img.save(self.avatar.path)

	def __str__(self):
		return f'Player: [ alias: {self.alias_name}, username: {self.username} ]'


class PlayerMatch(models.Model):
    id = models.AutoField(primary_key=True)
    match = models.ForeignKey('Match', on_delete=models.CASCADE, null=False, blank=False)
    player = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
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
	player = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
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
