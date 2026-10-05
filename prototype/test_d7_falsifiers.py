import subprocess
import sys
import unittest

import d7_falsifiers as F
import d7_sound_map as M


class FalsifierTests(unittest.TestCase):
    def test_every_row_claim_survives_its_falsifier(self):
        for name, fn in F.FALSIFIERS.items():
            ok, detail = fn()
            self.assertTrue(ok, f"{name}: {detail}")

    def test_the_commands_in_the_map_exit_zero(self):
        for row in M.rows()[:1] + M.rows()[3:4]:
            cmd = row[M.COLUMNS.index("falsifier_cmd")].split(" (and ")[0]
            self.assertEqual(subprocess.run(cmd.replace('cd prototype && ', ''), shell=True, capture_output=True).returncode, 0, cmd)

    def test_a_falsifier_fails_when_the_claim_is_false(self):
        original = F.L.SIGN_CELL.copy()
        try:
            F.L.SIGN_CELL["$"] = 127                    # claim: 24 of 32 ASCII punctuation characters
            self.assertFalse(F.f_ascii_signs()[0])
        finally:
            F.L.SIGN_CELL.clear()
            F.L.SIGN_CELL.update(original)


class PositionAttackTests(unittest.TestCase):
    def test_what_survives_a_permutation_of_the_places_and_members_of_the_varga_block(self):
        r = F.attack_positions()
        key = lambda name, kind: r[f"{name} (pairs {10 if name in ('asp', 'voice') else 20}) under {kind} permutations"]
        self.assertEqual(key("asp", "members")["constant add delta"], 24)       # arithmetic: only permutations that keep the +1 gap
        self.assertEqual(key("voice", "members")["constant add delta"], 24)
        self.assertEqual(key("nasal", "members")["constant add delta"], 0)      # never constant, not even unpermuted
        self.assertEqual(key("shift", "members")["constant add delta"], 120)    # +5 does not look at the member
        self.assertEqual(key("shift", "places")["constant add delta"], 2)       # identity and reversal only
        self.assertEqual(key("asp", "places")["constant add delta"], 120)
        for name in ("asp", "voice", "nasal", "shift"):
            for kind in ("members", "places"):
                self.assertEqual(key(name, kind)["constant xor delta"], 0)       # no xor law in the mixed radix, permuted or not
        self.assertEqual(r["savarṇa row relation (same place <=> same cell // 5) under place permutations"]["holds"], 120)

    def test_control_permuting_the_bit_positions_of_the_14_bit_code(self):
        self.assertEqual(F.attack_bit_positions(trials=50), {"asp": 50, "voice": 50, "of": 50})


if __name__ == "__main__":
    unittest.main()
