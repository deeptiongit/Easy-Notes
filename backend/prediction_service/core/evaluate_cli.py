"""Evaluation CLI wrapper.

Calls `evaluate_model` from `backend.prediction_service.core.evaluation` if available.
Writes a JSON metrics file to the `--out` path.
"""
import argparse
import sys
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model_dir', required=True)
    parser.add_argument('--eval_data', required=True)
    parser.add_argument('--out', required=True)
    parser.add_argument('--metric', default='f1')
    args = parser.parse_args()

    try:
        from backend.prediction_service.core.evaluation import evaluate_model
    except Exception:
        print('Evaluation function `evaluate_model` not found in repository.', file=sys.stderr)
        sys.exit(2)

    metrics = evaluate_model(model_dir=args.model_dir, eval_data_path=args.eval_data, metric=args.metric)
    with open(args.out, 'w') as f:
        json.dump(metrics, f)
    print('Wrote metrics to', args.out)


if __name__ == '__main__':
    main()
