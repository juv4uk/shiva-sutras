import os
import unittest

import upc7_phonetic_attack as A


@unittest.skipUnless(os.path.exists(A.DICT_UK) and A.KASIKA, "dict_uk or the Kasika is not checked out here")
class PhoneticAttackNumbers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.s = A.stats()

    def test_corpora(self):
        self.assertEqual((self.s["uk_lemmas_encoded"], self.s["sa_words_encoded"]), (229954, 40947))

    def test_what_the_four_close_pairs_buy_in_cross_layout_rendering(self):
        self.assertEqual((self.s["uk_renderable_in_sa_12"], self.s["uk_renderable_in_sa_16"]), (187, 551))
        self.assertEqual((self.s["sa_renderable_in_uk_12"], self.s["sa_renderable_in_uk_16"]), (107, 206))

    def test_homographs_across_layouts_are_made_by_the_unambiguous_pairs(self):
        self.assertEqual((self.s["homographs_12"], self.s["homographs_16"]), (18, 21))
        shown = {e[0] for e in self.s["homograph_examples"]}
        self.assertTrue({"kit", "nis", "su"} <= shown)

    def test_g_and_h_share_of_the_corpora(self):
        self.assertEqual((self.s["uk_lemmas_with_g(г)"], self.s["sa_words_with_h"]), (35183, 3976))


class ScriptProbe(unittest.TestCase):
    def test_r_ri_and_the_three_sibilants_stay_distinct(self):
        p = A.script_probe()
        self.assertNotEqual(p["sa-cyr:'р'"], p["sa-cyr:'р̣'"])
        self.assertTrue(p["sa-cyr:'р'"].endswith("= r") and p["sa-cyr:'р̣'"].endswith("= ṛ"))
        self.assertEqual(p["sa-cyr:'ш'"], "UnknownSpelling")                   # a bare ш is refused in the Sanskrit-Cyrillic layout, not guessed
        self.assertTrue(p["sa-cyr:'ш́'"].endswith("= ś") and p["sa-cyr:'ш̣'"].endswith("= ṣ"))
        self.assertEqual(p["uk:'ш'"], p["sa-cyr:'ш́'"].split(" = ")[0])        # uk ш is the cell of ś


if __name__ == "__main__":
    unittest.main()
