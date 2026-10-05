#!/usr/bin/env python3
"""Edge-computation benchmark: parity first, then Cachegrind I refs (setup vs full, median of 3), per edge and method.

    python3 prototype/bench_7bit/run_edges.py --out docs/upc7-edge-three-ways-bench-2026-10-02.tsv
"""
import argparse
import re
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
METHODS = "ABC"
NAMES = {"A": "guarded XOR on the 14-bit code", "B": "hand table mixed radix (7-bit)", "C": "lookup in 128 cells (7-bit)"}
EDGES = ("asp", "voice", "nasal", "shift", "long")


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def refs(binary, m, q, n, mode):
    with tempfile.NamedTemporaryFile("r", suffix=".vg") as log:
        subprocess.run(["valgrind", "--tool=cachegrind", "--cache-sim=no", "--cachegrind-out-file=/dev/null",
                        f"--log-file={log.name}", str(binary), m, q, str(n), mode], check=True, capture_output=True)
        return int(re.search(r"I\s+refs:\s+([\d,]+)", Path(log.name).read_text()).group(1).replace(",", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--calls", type=int, default=200000)
    ap.add_argument("--repeats", type=int, default=3)
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as t:
        binary = Path(t) / "bench_edges"
        (HERE / "edges.h").write_text(sh([sys.executable, str(HERE / "gen_edges.py")]))
        sh(["gcc", "-O2", "-Wall", "-Wextra", "-o", str(binary), str(HERE / "bench_edges.c")])
        out = [f"# gcc: {sh(['gcc', '--version']).splitlines()[0]}", f"# valgrind: {sh(['valgrind', '--version']).strip()}"]
        for m in METHODS:
            out += ["# " + line for line in sh([str(binary), m, "asp", "0", "check"]).strip().splitlines()]
        out.append("\t".join(["method", "name", "edge", "I_per_call_gross", "I_per_call_net_of_null", "I_setup_extra"]))
        med = lambda m, q, mode: int(statistics.median(refs(binary, m, q, a.calls, mode) for _ in range(a.repeats)))
        null = (med("A", "null", "full") - med("A", "null", "setup")) / a.calls
        for m in METHODS:
            for q in EDGES:
                per = (med(m, q, "full") - med(m, q, "setup")) / a.calls
                out.append("\t".join([m, NAMES[m], q, f"{per:.2f}", f"{per - null:.2f}", str(med(m, q, "setup") - med("A", q, "setup"))]))
        out.append("\t".join(["-", "null (loop + rng)", "null", f"{null:.2f}", "0.00", "0"]))
        Path(a.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
