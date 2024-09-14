from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from .enums import State, Status, StatusChoices

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

	class Meta:
		verbose_name_plural = 'Profils'

	def __str__(self):
		return self.user.username

	def save(self, *args, **kwargs):
		super().save(*args, **kwargs)
		if self.photo:
			img = Image.open(self.photo.path)
			if img.height > 600 or img.width > 600:
				output_size = (600,600)
				img.thumbnail(output_size)
				img.save(self.photo.path)


class ProfileComment(models.Model):
	user_profil = models.ForeignKey(Profil, on_delete=models.CASCADE)
	comment_text = models.CharField(max_length=300)
	create_time = models.DateTimeField(auto_now_add=True)
	update_time = models.DateTimeField(auto_now=True)

	class Meta:
		verbose_name_plural = 'ProfileCommand'

	def __str__(self):
		return str(self.user_profil.user.username)

class UserFriendsList(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_friend_requests')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_friend_requests')

    friend_request = models.BooleanField(default=False)
    create_time = models.DateTimeField(auto_now_add=True)
    update_time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'UserFriendsList'
        unique_together = ('sender', 'receiver')

    def __str__(self):
        return f'{self.sender.username} -> {self.receiver.username}'

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
