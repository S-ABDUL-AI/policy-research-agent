#!/usr/bin/env python3
"""
CLI entry point.

Usage:
    python run.py "What is the evidence on SNAP benefit cliffs and work disincentives?"
    python run.py "What are the equity implications of AI-driven Medicaid eligibility tools?" --output results/medicaid
"""

import argparse
import sys
from agent import run_agent


def main():
    parser = argparse.ArgumentParser(
        description="Policy Research Agent with behavioral self-monitoring"
    )
    parser.add_argument(
        "question",
        type=str,
        help="The policy question to research",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Directory for output files (default: output/)",
    )
    args = parser.parse_args()

    if not args.question.strip():
        print("Error: question cannot be empty.")
        sys.exit(1)

    result = run_agent(args.question, output_dir=args.output)
    print("\nDone.")


if __name__ == "__main__":
    main()
