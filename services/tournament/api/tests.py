from django.test import TestCase
from .models import User, Tournament, Match, PlayerMatch, PlayerTournament
from .enums import Round, State, Status, StatusChoices

class QueryTestCase(TestCase):
    def setUp(self):
        # Create User instances
        user1 = User.objects.create(username="irem_ozt", email="irem@example.com", alias_name="ioztimur", wins=10, losses=5, status=Status.OFFLINE.value, championships=2127983)
        user2 = User.objects.create(username="zort", email="zort@example.com", alias_name="zorttttt", wins=0, losses=5, status=Status.OFFLINE.value, championships=1)

        # Create Tournament instances
        tournament1 = Tournament.objects.create(name="Summer 42 Cup", round=Round.HALF.value, status=StatusChoices.PENDING.value)

        # Create Match instances
        match1 = Match.objects.create(tournament=tournament1, round=Round.HALF.value, state=State.UNPLAYED.value)
        match2 = Match.objects.create(tournament=tournament1, round=Round.QUARTER.value, state=State.PLAYED.value)

        # Create PlayerMatch instances
        player_match1 = PlayerMatch.objects.create(match_id=match1, player_id=user1, score=100, won=True)
        player_match2 = PlayerMatch.objects.create(match_id=match2, player_id=user2, score=150, won=False)

		# Create PlayerTournament instances
        player_tournament1 = PlayerTournament.objects.create(tournament_id=tournament1, player_id=user1, creator=True)
        player_tournament2 = PlayerTournament.objects.create(tournament_id=tournament1, player_id=user2, creator=False)

    def test_queries(self):
        # Get all users
        users = User.objects.all()
        for user in users:
            print(user)

        # Get all tournaments
        tournaments = Tournament.objects.all()
        for tournament in tournaments:
            print(tournament)

        # Get all matches
        matches = Match.objects.all()
        for match in matches:
            print(match)

        # Get all player matches
        player_matches = PlayerMatch.objects.all()
        for player_match in player_matches:
            print(player_match)

        # Get all player tournaments
        player_tournaments = PlayerTournament.objects.all()
        for player_tournament in player_tournaments:
            print(player_tournament)
