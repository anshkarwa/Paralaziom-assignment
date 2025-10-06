# api/views.py
from django.db.models import Count, Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Match, Delivery

class MatchesPerYearView(APIView):
    """
    API endpoint for Task 1: Plot the number of matches played per year.
    """
    def get(self, request, format=None):
        data = (
            Match.objects.values('season')
            .annotate(matches_played=Count('id'))
            .order_by('season')
        )
        return Response(data)

class MatchesWonOverYearsView(APIView):
    """
    API endpoint for Task 2: Plot a stacked bar chart of matches won of all teams.
    """
    def get(self, request, format=None):
        data = (
            Match.objects.exclude(winner__isnull=True).exclude(winner="")
            .values('season', 'winner')
            .annotate(wins=Count('winner'))
            .order_by('season', 'winner')
        )
        return Response(data)

class ExtraRunsConcededView(APIView):
    """
    API endpoint for Task 3: For a year "YYYY", plot extra runs conceded per team.
    """
    def get(self, request, format=None):
        year = request.query_params.get('year')
        if not year:
            return Response({"error": "Year parameter is required."}, status=400)

        # Get all match IDs for the given season (year)
        match_ids = Match.objects.filter(season=year).values_list('id', flat=True)

        data = (
            Delivery.objects.filter(match_id__in=match_ids)
            .values('bowling_team')
            .annotate(extra_runs=Sum('extra_runs'))
            .order_by('-extra_runs')
        )
        return Response(data)