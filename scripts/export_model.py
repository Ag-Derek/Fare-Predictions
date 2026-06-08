#!/usr/bin/env python3
"""
export_model.py — Export fare_model.pkl + encoders.pkl → public/model.json

Usage:
    python scripts/export_model.py
    python scripts/export_model.py --model path/to/fare_model.pkl --encoders path/to/encoders.pkl
"""
import argparse, json, os, sys
from pathlib import Path

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model',    default='fare_model.pkl')
    parser.add_argument('--encoders', default='encoders.pkl')
    parser.add_argument('--out',      default='public/model.json')
    args = parser.parse_args()

    try:
        import joblib
    except ImportError:
        sys.exit("Run: pip install joblib scikit-learn")

    print(f"Loading model from {args.model}...")
    model    = joblib.load(args.model)
    encoders = joblib.load(args.encoders)

    if type(model).__name__ != 'RandomForestRegressor':
        sys.exit(f"Expected RandomForestRegressor, got {type(model).__name__}")

    print(f"Exporting {len(model.estimators_)} trees...")

    def export_tree(tree):
        t = tree.tree_
        return {
            'f':  t.feature.tolist(),
            'th': [round(float(x), 6) for x in t.threshold],
            'l':  t.children_left.tolist(),
            'r':  t.children_right.tolist(),
            'v':  [round(float(x[0][0]), 4) for x in t.value],
        }

    model_json = {
        'trees': [export_tree(est) for est in model.estimators_],
        'encoders': {k: list(v.classes_) for k, v in encoders.items()},
    }

    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    json_str = json.dumps(model_json, separators=(',', ':'))

    with open(out_path, 'w') as f:
        f.write(json_str)

    size_kb = len(json_str) / 1024
    print(f"✅ Saved {out_path} ({size_kb:.0f} KB)")
    print(f"   Tip: gzip compresses this to ~{size_kb*0.31:.0f} KB over the wire")

if __name__ == '__main__':
    main()
