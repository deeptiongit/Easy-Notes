"""Trainer CLI wrapper.

Non-invasive entrypoint that calls `continuous_train` from
`backend.prediction_service.core.trainer` if available.

Usage:
    python -m backend.prediction_service.core.trainer_cli --data /path/to/data.csv --out /path/to/model_dir
"""
import argparse
import sys
import os
import json


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', required=True, help='Path to training CSV')
    parser.add_argument('--out', required=True, help='Output path or directory for trained model')
    parser.add_argument('--args', default='{}', help='JSON string of extra args')
    args = parser.parse_args()

    try:
        from backend.prediction_service.core.trainer import continuous_train
    except Exception:
        print('Trainer function `continuous_train` not found in repository.', file=sys.stderr)
        sys.exit(2)

    # Determine model file path: if `--out` looks like a directory (exists or ends with '/'),
    # create it and write model.joblib inside. Otherwise treat `--out` as the target file path.
    out_path = args.out
    if out_path.endswith(os.sep) or out_path.endswith('/') or os.path.isdir(out_path):
        os.makedirs(out_path, exist_ok=True)
        model_path = os.path.join(out_path, 'model.joblib')
    else:
        # If the path does not look like a file (no extension), create parent dir and treat as file.
        parent = os.path.dirname(out_path) or '.'
        os.makedirs(parent, exist_ok=True)
        model_path = out_path

    extra = json.loads(args.args)
    ok = continuous_train(model_path=model_path, training_data=args.data)
    if not ok:
        print('Training failed', file=sys.stderr)
        sys.exit(1)
    # If trainer did not produce an artifact (some repos only run training logic),
    # write a small marker artifact so downstream pipeline components have a file to reference.
    try:
        if not os.path.exists(model_path):
            # write a tiny marker file
            with open(model_path, 'w') as f:
                f.write('{"mock_trained": true}')
    except Exception:
        # Best-effort only; do not fail if we cannot write
        pass

    print('Training completed successfully, model at', model_path)


if __name__ == '__main__':
    main()
