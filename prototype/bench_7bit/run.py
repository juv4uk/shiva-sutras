#!/usr/bin/env python3
"""Run the design-level 7-bit query benchmark: parity first, then Cachegrind I refs (setup vs full). Per-call numbers are GROSS: the call loop and the rng are included and are the same for every design (the `null` query measures them); read DIFFERENCES between designs.

    python3 prototype/bench_7bit/run.py --out docs/research/7bit-design-query-bench-2026-10-01.tsv
"""
import argparse
import re
import statistics
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
DESIGNS = "HDVATL"
NAMES = {"H": "hand table", "D": "saṅkṣepa7 (derived)", "V": "varṇa7", "A": "akṣara7", "T": "tantu7", "L": "legacy (sutra order)"}


def sh(cmd):
    return subprocess.run(cmd, check=True, capture_output=True, text=True).stdout


def refs(binary, d, q, n, mode):
    with tempfile.NamedTemporaryFile("r", suffix=".vg") as log:
        subprocess.run(["valgrind", "--tool=cachegrind", "--cache-sim=no", "--cachegrind-out-file=/dev/null",
                        f"--log-file={log.name}", str(binary), d, q, str(n), mode], check=True, capture_output=True)
        return int(re.search(r"I\s+refs:\s+([\d,]+)", Path(log.name).read_text()).group(1).replace(",", ""))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--calls", type=int, default=200000)
    ap.add_argument("--repeats", type=int, default=3)
    a = ap.parse_args()
    with tempfile.TemporaryDirectory() as t:
        binary = Path(t) / "bench7"
        (HERE / "tables.h").write_text(sh([sys.executable, str(HERE / "gen_tables.py")]))
        sh(["gcc", "-O2", "-Wall", "-Wextra", "-o", str(binary), str(HERE / "bench7.c")])
        out = [f"# gcc: {sh(['gcc', '--version']).splitlines()[0]}", f"# valgrind: {sh(['valgrind', '--version']).strip()}"]
        for d in DESIGNS:
            out.append("# " + sh([str(binary), d, "sav", "0", "check"]).strip())
        out.append("\t".join(["design", "name", "query", "I_per_call_gross", "I_setup_extra"]))
        med = lambda d, q, mode: int(statistics.median(refs(binary, d, q, a.calls, mode) for _ in range(a.repeats)))
        for d in DESIGNS:
            for q in ("null", "sav", "ac", "jhal"):
                per = (med(d, q, "full") - med(d, q, "setup")) / a.calls     # gross: the call loop and rng are included
                out.append("\t".join([d, NAMES[d], q, f"{per:.2f}", str(med(d, q, "setup") - med("H", q, "setup"))]))
        Path(a.out).write_text("\n".join(out) + "\n", encoding="utf-8")
    print("wrote", a.out)


if __name__ == "__main__":
    main()
