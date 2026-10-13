"""Exact continuous-time quantum-walk search on a complete graph.

The invariant two-dimensional subspace is spanned by the marked vertex
and the uniform superposition of unmarked vertices. No quantum hardware,
large graph matrix or external numerical dependency is required.
"""
import argparse
import csv
import json
import math
import sys
from pathlib import Path
from typing import Optional


def simulate_complete_graph(
    node_count: int = 16,
    marked_vertex: int = 0,
    gamma: Optional[float] = None,
    max_time: Optional[float] = None,
    samples: int = 201,
) -> dict:
    """Return sampled marked-vertex probabilities under H = -gamma*A - |w><w|.

    Initial state is the uniform superposition over every vertex. The graph
    is K_N with zero-diagonal adjacency; evolution uses hbar=1.
    """
    if isinstance(node_count, bool) or not isinstance(node_count, int) or not 2 <= node_count <= 100_000:
        raise ValueError("node_count must be an integer between 2 and 100000")
    if isinstance(marked_vertex, bool) or not isinstance(marked_vertex, int) or not 0 <= marked_vertex < node_count:
        raise ValueError("marked_vertex must be an integer within the graph")
    if isinstance(samples, bool) or not isinstance(samples, int) or not 2 <= samples <= 2001:
        raise ValueError("samples must be an integer between 2 and 2001")
    gamma = 1.0 / node_count if gamma is None else gamma
    if not isinstance(gamma, (int, float)) or isinstance(gamma, bool) or not math.isfinite(gamma) or gamma <= 0:
        raise ValueError("gamma must be positive and finite")
    max_time = math.pi * math.sqrt(node_count) / 2 if max_time is None else max_time
    if not isinstance(max_time, (int, float)) or isinstance(max_time, bool) or not math.isfinite(max_time) or not 0 < max_time <= 100_000:
        raise ValueError("max_time must be finite and in (0, 100000]")

    # H in {|marked>, uniform(|unmarked>)} basis.
    delta = (-1.0 + gamma * (node_count - 2)) / 2.0
    offdiag = -gamma * math.sqrt(node_count - 1)
    omega = math.hypot(delta, offdiag)
    initial_marked = 1.0 / math.sqrt(node_count)
    initial_unmarked = math.sqrt((node_count - 1) / node_count)
    transfer = (delta * initial_marked + offdiag * initial_unmarked) / omega

    series = []
    for index in range(samples):
        time = float(max_time) * index / (samples - 1)
        phase = omega * time
        probability = (initial_marked * math.cos(phase)) ** 2 + (transfer * math.sin(phase)) ** 2
        # Bound floating-point roundoff without masking a material model error.
        probability = min(1.0, max(0.0, probability))
        series.append({"time": time, "success_probability": probability})
    best = max(series, key=lambda point: point["success_probability"])
    return {
        "model": "continuous-time quantum walk on complete graph",
        "hamiltonian": "H = -gamma*A - |w><w|",
        "node_count": node_count,
        "marked_vertex": marked_vertex,
        "gamma": float(gamma),
        "max_time": float(max_time),
        "samples": samples,
        "initial_probability": 1.0 / node_count,
        "peak_time": best["time"],
        "peak_success_probability": best["success_probability"],
        "series": series,
    }


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Exact CTQW spatial search on a complete graph")
    parser.add_argument("--nodes", type=int, default=16, help="number of vertices (2..100000)")
    parser.add_argument("--marked", type=int, default=0, help="marked vertex index (zero-based)")
    parser.add_argument("--gamma", type=float, help="hopping rate (default 1/N)")
    parser.add_argument("--max-time", type=float, help="simulation duration (default pi*sqrt(N)/2)")
    parser.add_argument("--samples", type=int, default=201, help="number of samples (2..2001)")
    parser.add_argument("--csv", type=Path, help="optional CSV output path")
    args = parser.parse_args(argv)
    try:
        result = simulate_complete_graph(args.nodes, args.marked, args.gamma, args.max_time, args.samples)
    except ValueError as exc:
        parser.error(str(exc))
    if args.csv:
        try:
            with args.csv.open("w", newline="", encoding="utf-8") as output:
                writer = csv.DictWriter(output, fieldnames=["time", "success_probability"])
                writer.writeheader()
                writer.writerows(result["series"])
        except OSError as exc:
            parser.exit(1, f"Cannot write CSV: {exc}\n")
        print(f"Saved {len(result['series'])} samples to {args.csv}")
    else:
        json.dump(result, sys.stdout, indent=2)
        print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
