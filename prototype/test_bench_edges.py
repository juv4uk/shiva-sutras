import os
import shutil
import subprocess
import sys
import tempfile
import unittest

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "bench_7bit")


@unittest.skipUnless(shutil.which("gcc"), "gcc is not installed here")
class EdgeBenchParityTests(unittest.TestCase):
    def test_parity_before_any_timing(self):
        with tempfile.TemporaryDirectory() as t:
            header = subprocess.run([sys.executable, os.path.join(HERE, "gen_edges.py")], check=True, capture_output=True, text=True).stdout
            open(os.path.join(t, "edges.h"), "w").write(header)
            binary = os.path.join(t, "be")
            subprocess.run(["gcc", "-O2", "-I", t, "-o", binary, os.path.join(HERE, "bench_edges.c")], check=True)
            got = {}
            for m in "ABC":
                for line in subprocess.run([binary, m, "asp", "0", "check"], check=True, capture_output=True, text=True).stdout.splitlines():
                    _, method, edge, pairs, bad = line.split("\t")
                    got[(method, edge)] = (int(pairs.split("=")[1]), int(bad.split("=")[1]))
        self.assertEqual({k: v[0] for k, v in got.items() if k[0] == "A"}, {("A", "asp"): 20, ("A", "voice"): 20, ("A", "nasal"): 20, ("A", "shift"): 30, ("A", "long"): 4})
        mismatches = {k: v[1] for k, v in got.items() if v[1]}
        self.assertEqual(mismatches, {("B", "shift"): 5})        # the hand table's radix cannot do y->r, r->l, i->ṛ, ī->ṝ, ḷ->u


if __name__ == "__main__":
    unittest.main()
