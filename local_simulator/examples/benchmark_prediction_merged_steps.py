"""Benchmark shared per-step work against the prior native bridge dispatch."""
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from local_simulator.examples.benchmark_prediction_random_acceleration import main

if __name__ == '__main__':
    main(stage='merged')
