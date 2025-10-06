# api/management/commands/load_data.py
import pandas as pd
from django.core.management.base import BaseCommand
from api.models import Match, Delivery
from django.db import transaction

class Command(BaseCommand):
    help = 'Load data from CSV files into the database'

    @transaction.atomic
    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Deleting old data...'))
        Delivery.objects.all().delete()
        Match.objects.all().delete()

        # --- Load Matches Data ---
        try:
            matches_df = pd.read_csv('data/matches.csv')
            matches_to_create = []
            for _, row in matches_df.iterrows():
                # Convert date string to date object
                date_obj = pd.to_datetime(row['date']).date()
                matches_to_create.append(
                    Match(
                        id=row['id'],
                        season=row['season'],
                        city=row['city'],
                        date=date_obj,
                        team1=row['team1'],
                        team2=row['team2'],
                        toss_winner=row['toss_winner'],
                        toss_decision=row['toss_decision'],
                        result=row['result'],
                        dl_applied=bool(row['dl_applied']),
                        winner=row['winner'],
                        win_by_runs=row['win_by_runs'],
                        win_by_wickets=row['win_by_wickets'],
                        player_of_match=row['player_of_match'],
                        venue=row['venue'],
                        umpire1=row['umpire1'],
                        umpire2=row['umpire2'],
                        umpire3=row['umpire3']
                    )
                )
            
            Match.objects.bulk_create(matches_to_create)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(matches_to_create)} matches.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading matches: {e}'))
            return # Stop if matches fail to load

        # --- Load Deliveries Data ---
        try:
            deliveries_df = pd.read_csv('data/deliveries.csv')
            # Create a dictionary for quick match lookups
            all_matches = {match.id: match for match in Match.objects.all()}
            
            deliveries_to_create = []
            for _, row in deliveries_df.iterrows():
                match_instance = all_matches.get(row['match_id'])
                if match_instance: # Only create delivery if its match exists
                    deliveries_to_create.append(
                        Delivery(
                            match=match_instance,
                            inning=row['inning'],
                            batting_team=row['batting_team'],
                            bowling_team=row['bowling_team'],
                            over=row['over'],
                            ball=row['ball'],
                            batsman=row['batsman'],
                            non_striker=row['non_striker'],
                            bowler=row['bowler'],
                            is_super_over=bool(row['is_super_over']),
                            wide_runs=row['wide_runs'],
                            bye_runs=row['bye_runs'],
                            legbye_runs=row['legbye_runs'],
                            noball_runs=row['noball_runs'],
                            penalty_runs=row['penalty_runs'],
                            batsman_runs=row['batsman_runs'],
                            extra_runs=row['extra_runs'],
                            total_runs=row['total_runs'],
                            player_dismissed=row['player_dismissed'],
                            dismissal_kind=row['dismissal_kind'],
                            fielder=row['fielder']
                        )
                    )

            Delivery.objects.bulk_create(deliveries_to_create, batch_size=1000)
            self.stdout.write(self.style.SUCCESS(f'Successfully loaded {len(deliveries_to_create)} deliveries.'))

        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error loading deliveries: {e}'))