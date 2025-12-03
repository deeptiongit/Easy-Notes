"""Preprocess CLI wrapper.

Calls `preprocess_main` in `backend.prediction_service.core.preprocess` if available.
"""
import argparse
import sys
import os


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--in', dest='inp', required=True)
    parser.add_argument('--out', dest='out', required=True)
    args = parser.parse_args()

    try:
        from backend.prediction_service.core.preprocess import preprocess_main
    except Exception:
        print('Preprocess entrypoint `preprocess_main` not found in repository.', file=sys.stderr)
        sys.exit(2)

    preprocess_main(input_path=args.inp, output_path=args.out)
    print('Preprocessing completed:', args.out)


if __name__ == '__main__':
    main()
