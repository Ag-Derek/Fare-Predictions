#!/usr/bin/env python3
"""
export_stats.py — Generate public/stats.json from the ride-sharing CSV.

Usage:
    python scripts/export_stats.py
    python scripts/export_stats.py --csv data/ghana_ride_sharing_synthetic.csv
"""
import argparse, json
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--csv', default='ghana_ride_sharing_synthetic.csv')
    parser.add_argument('--out', default='public/stats.json')
    args = parser.parse_args()

    try:
        import pandas as pd
    except ImportError:
        import sys; sys.exit("Run: pip install pandas")

    df = pd.read_csv(args.csv)
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['hour'] = df['start_time'].dt.hour

    stats = {
        'fare_by_city':    df.groupby('city')['fare'].agg(['mean','min','max','median']).round(2).reset_index().to_dict('records'),
        'fare_by_payment': df.groupby('payment_method')['fare'].mean().round(2).reset_index().to_dict('records'),
        'fare_by_hour':    [{'hour': int(r['hour']), 'fare': round(float(r['fare']), 2)}
                            for _, r in df.groupby('hour')['fare'].mean().reset_index().iterrows()],
        'overall': {
            'total_trips':   len(df),
            'avg_fare':      round(float(df['fare'].mean()), 2),
            'avg_distance':  round(float(df['distance_km'].mean()), 2),
            'avg_duration':  round(float(df['duration_min'].mean()), 1),
        }
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with open(out_path, 'w') as f:
        json.dump(stats, f, separators=(',', ':'))

    print(f"✅ Saved {out_path}")

if __name__ == '__main__':
    main()
