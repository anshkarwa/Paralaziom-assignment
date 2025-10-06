# api/models.py
from django.db import models

class Match(models.Model):
    id = models.IntegerField(primary_key=True)
    season = models.IntegerField()
    city = models.CharField(max_length=100, null=True, blank=True)
    date = models.DateField()
    team1 = models.CharField(max_length=100)
    team2 = models.CharField(max_length=100)
    toss_winner = models.CharField(max_length=100)
    toss_decision = models.CharField(max_length=10)
    result = models.CharField(max_length=20)
    dl_applied = models.BooleanField()
    winner = models.CharField(max_length=100, null=True, blank=True)
    win_by_runs = models.IntegerField()
    win_by_wickets = models.IntegerField()
    player_of_match = models.CharField(max_length=100, null=True, blank=True)
    venue = models.CharField(max_length=200)
    umpire1 = models.CharField(max_length=100, null=True, blank=True)
    umpire2 = models.CharField(max_length=100, null=True, blank=True)
    umpire3 = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'{self.team1} vs {self.team2} ({self.season})'

class Delivery(models.Model):
    match = models.ForeignKey(Match, on_delete=models.CASCADE)
    inning = models.IntegerField()
    batting_team = models.CharField(max_length=100)
    bowling_team = models.CharField(max_length=100)
    over = models.IntegerField()
    ball = models.IntegerField()
    batsman = models.CharField(max_length=100)
    non_striker = models.CharField(max_length=100)
    bowler = models.CharField(max_length=100)
    is_super_over = models.BooleanField()
    wide_runs = models.IntegerField()
    bye_runs = models.IntegerField()
    legbye_runs = models.IntegerField()
    noball_runs = models.IntegerField()
    penalty_runs = models.IntegerField()
    batsman_runs = models.IntegerField()
    extra_runs = models.IntegerField()
    total_runs = models.IntegerField()
    player_dismissed = models.CharField(max_length=100, null=True, blank=True)
    dismissal_kind = models.CharField(max_length=100, null=True, blank=True)
    fielder = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f'Match {self.match.id} - {self.batting_team} - Over {self.over}'