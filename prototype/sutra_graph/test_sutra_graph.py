#!/usr/bin/env python3
"""Logic test of the extractor on a SYNTHETIC fixture (invented mini data in the dataset's shape; [FIXTURE])."""
import csv, json, os, subprocess, sys, tempfile, unittest

HERE = os.path.dirname(os.path.abspath(__file__))

def sut(a, p, n, text, an="", ad=""):
    return {"a": str(a), "p": str(p), "n": str(n), "s": text, "an": an, "ad": ad, "type": "V$$"}

DATA = [
    sut(6, 1, 84, "एकः पूर्वपरयोः"),
    sut(6, 1, 87, "आद् गुणः", ad="एकः पूर्वपरयोः$6$1$84"),
    sut(6, 1, 88, "वृद्धिरेचि", an="आत्$61087##एकः$61084", ad="एकः पूर्वपरयोः$6$1$84"),
    sut(6, 1, 97, "अतो गुणे", an="अतः$61087", ad="एकः पूर्वपरयोः$6$1$84"),
    sut(6, 1, 101, "अकः सवर्णे दीर्घः", ad="एकः पूर्वपरयोः$6$1$84"),
]
KASIKA = {
    "61088": "आद्गुणस्यापवादः। ब्रह्मैडका॥",
    "61097": "अकः सवर्णे दीर्घस्य [[६.१.१०१]] अपवादः। पचे॥",
    "61101": "सवर्णे इति किम्? दध्यत्र॥",
}

class ExtractorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.mkdtemp()
        src = os.path.join(cls.tmp, "src"); os.makedirs(src)
        json.dump({"name": "sutraani", "data": DATA}, open(os.path.join(src, "data.txt"), "w", encoding="utf-8"), ensure_ascii=False)
        json.dump(KASIKA, open(os.path.join(src, "kashika.txt"), "w", encoding="utf-8"), ensure_ascii=False)
        out = os.path.join(cls.tmp, "out")
        subprocess.run([sys.executable, os.path.join(HERE, "build_sutra_graph.py"), src, out], check=True, capture_output=True)
        cls.edges = [tuple(r) for r in csv.reader(open(os.path.join(out, "edges.tsv"), encoding="utf-8"), delimiter="\t")][1:]

    def has(self, s, d, kind):
        return any(e[0] == s and e[1] == d and e[2] == kind for e in self.edges)

    def test_anuvrtti_ids_are_read_as_sutra_numbers(self):
        self.assertTrue(self.has("6.1.88", "6.1.87", "anuvrtti"))
        self.assertTrue(self.has("6.1.88", "6.1.84", "anuvrtti"))

    def test_adhikara_edges(self):
        self.assertTrue(self.has("6.1.87", "6.1.84", "adhikara"))

    def test_a_devanagari_digit_reference_becomes_an_edge(self):
        self.assertTrue(self.has("6.1.97", "6.1.101", "kasika_ref"))

    def test_apavada_by_explicit_reference(self):
        self.assertTrue(self.has("6.1.97", "6.1.101", "apavada"))

    def test_apavada_by_a_quoted_name_resolved_against_the_sutra_text(self):
        self.assertTrue(self.has("6.1.88", "6.1.87", "apavada"))

    def test_no_invented_edges(self):
        self.assertFalse(self.has("6.1.101", "6.1.97", "apavada"))

if __name__ == "__main__":
    unittest.main()
