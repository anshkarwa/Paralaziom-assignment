# api/urls.py
from django.urls import path
from .views import MatchesPerYearView, MatchesWonOverYearsView, ExtraRunsConcededView

urlpatterns = [
    path('matches-per-year/', MatchesPerYearView.as_view(), name='matches-per-year'),
    path('matches-won/', MatchesWonOverYearsView.as_view(), name='matches-won'),
    path('extra-runs/', ExtraRunsConcededView.as_view(), name='extra-runs'),
]