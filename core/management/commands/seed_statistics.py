import random
from datetime import date, timedelta
from django.core.management.base import BaseCommand
from core.models import PlacementStatistic

class Command(BaseCommand):
    help = "Seed 365 days of placement statistics"

    def handle(self, *args, **kwargs):

        PlacementStatistic.objects.all().delete()

        statistics = []

        today = date.today()

        for i in range(365):
            day = today - timedelta(days=i)

            stats = PlacementStatistic(
                date=day,
                total_placed=random.randint(0, 15),
                average_package_lpa=round(random.uniform(3.0, 15.0), 2),
            )

            statistics.append(stats)

        PlacementStatistic.objects.bulk_create(statistics)
        self.stdout.write(self.style.SUCCESS("✅ Seeded 1-year placement statistics"))
