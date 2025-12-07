# core/management/commands/train_ml.py
from django.core.management.base import BaseCommand
import pandas as pd
import numpy as np
from core.ml_models import train_models
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Train ML models for placement prediction. If no dataset present, synthetic data will be generated.'

    def add_arguments(self, parser):
        parser.add_argument('--data', type=str, help='CSV file path to training data (optional)')
        parser.add_argument('--force', action='store_true', help='Retrain even if models exist')

    def handle(self, *args, **options):
        data_path = options.get('data')
        force = options.get('force', False)

        # If user provided CSV, read it
        if data_path:
            if not os.path.exists(data_path):
                self.stdout.write(self.style.ERROR(f"Data file not found: {data_path}"))
                return
            df = pd.read_csv(data_path)
        else:
            # generate synthetic data
            self.stdout.write("No data provided — generating synthetic dataset (for demo only).")
            np.random.seed(0)
            N = 2000
            branches = ['CSE', 'ECE', 'MECH', 'CIVIL', 'IT']
            df = pd.DataFrame({
                'branch': np.random.choice(branches, size=N, p=[0.35,0.25,0.15,0.1,0.15]),
                'cgpa': np.round(np.random.normal(7.0, 1.0, size=N).clip(4.0,10.0), 2),
                'year': np.random.choice([2023,2024,2025], size=N, p=[0.3,0.4,0.3])
            })
            # synthetic placement label: probability depends on cgpa and branch
            def synth_label(row):
                base = (row['cgpa'] - 6.0) * 0.4
                branch_boost = 0.2 if row['branch'] in ('CSE','IT') else 0.0
                prob = (0.2 + base + branch_boost)
                prob = max(0.01, min(0.99, prob))
                return np.random.rand() < prob
            df['placed'] = df.apply(synth_label, axis=1).astype(int)
            # package: if placed, depends on cgpa and randomness
            def synth_package(row):
                if row['placed']:
                    base = 4.0 + (row['cgpa'] - 6.0) * 1.5
                    # branch multiplier
                    mult = 1.3 if row['branch']=='CSE' else (1.1 if row['branch']=='IT' else 0.9)
                    val = max(2.0, base * mult + np.random.normal(0, 1.0))
                    return round(float(val), 2)
                return 0.0
            df['package_lpa'] = df.apply(synth_package, axis=1)

        self.stdout.write(f"Training on {len(df)} rows.")
        metrics = train_models(df)
        self.stdout.write(self.style.SUCCESS("Training complete."))
        self.stdout.write(str(metrics))
