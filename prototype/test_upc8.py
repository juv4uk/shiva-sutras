#!/usr/bin/env python3
"""
Test suite for UPC-8 prototype.
Run: python test_upc8.py
"""

import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from upc8 import UPC8, CANON_POSITIONS, SIVA_SUTRAS, CODE_OF_POSITION, ALIASES, canon_ref, canon_source_matches


def test_canon_source_provenance():
    """Drift detector, not a correctness proof: SIVA_SUTRAS is a manual
    SLP1 transcription of ksetra/canon/siva-sutras.yaml. If that source
    file changes, this must fail loudly instead of silently going stale."""
    assert canon_source_matches(), (
        "ksetra/canon/siva-sutras.yaml has changed since SIVA_SUTRAS in "
        "upc8.py was transcribed from it -- update SIVA_SUTRAS and "
        "CANON_SOURCE_SHA256, do not just bump the hash to silence this."
    )
    print("  [PASS] Canon source provenance: SIVA_SUTRAS matches ksetra/canon/siva-sutras.yaml hash")


def test_canon_completeness():
    assert len(SIVA_SUTRAS) == 14
    assert len(CANON_POSITIONS) == 43
    slp1_set = set(p["slp1"] for p in CANON_POSITIONS)
    assert len(slp1_set) == 42  # h duplicated
    assert len(ALIASES) == 1, f"Expected 1 alias (h), got {len(ALIASES)}"
    print("  [PASS] Canon: 14 sutras, 43 positions, 42 unique sounds, 1 alias (h)")


def test_canonical_codes():
    u = UPC8()
    assert u.encode_sanskrit("a") == 0x00
    assert u.encode_sanskrit("i") == 0x01
    assert u.encode_sanskrit("u") == 0x02
    # Last canonical code is 0x29 = 41 decimal (42 codes: 0x00-0x29)
    assert 0x29 in u.table
    assert u.table[0x29]["layer"] == "canonical"
    # Sanskrit extended starts at 0x2A
    assert u.decode(0x2A)["layer"] == "sanskrit_extended"
    print("  [PASS] Canonical codes 0x00-0x29 (42 unique), extended starts at 0x2A")


def test_sanskrit_extended():
    u = UPC8()
    assert u.decode(0x2A)["iast"] == "a:"
    assert u.decode(0x2B)["iast"] == "i:"
    assert u.decode(0x2C)["iast"] == "u:"
    assert u.decode(0x2F)["iast"] == "~"   # anusvara
    assert u.decode(0x30)["iast"] == "H"   # visarga
    print("  [PASS] Sanskrit extended codes 0x2A-0x30 (7 sounds)")


def test_ukrainian_shared():
    u = UPC8()
    assert u.encode_ukrainian("\u0456") == 0x01  # i shares with Sanskrit i
    assert u.encode_ukrainian("\u0443") == 0x02  # u shares with Sanskrit u
    assert u.encode_ukrainian("\u0431") == 0x19  # b shares with Sanskrit b
    info = u.decode(0x01)
    assert "ukrainian" in info.get("languages", {})
    assert info["languages"]["ukrainian"]["relation"] == "segment-equivalent"
    print("  [PASS] Ukrainian shared codes reuse canonical codes (13 shared)")


def test_ukrainian_new():
    u = UPC8()
    assert u.encode_ukrainian("\u0438") == 0x31  # y (и)
    assert u.encode_ukrainian("\u0448") == 0x3B  # sh (ш)
    assert u.encode_ukrainian("\u0449") == 0x4A  # shch (щ)
    assert u.decode(0x4F)["layer"] == "ukrainian_new"
    print("  [PASS] Ukrainian new codes 0x31-0x4F (31 new)")


def test_word_encoding_sanskrit():
    u = UPC8()
    encoded = u.encode_sanskrit_word("karma")
    assert encoded == bytes([0x25, 0x00, 0x0C, 0x0F, 0x00])
    decoded = u.decode_bytes(encoded)
    assert "".join(d.get("slp1", "?") for d in decoded) == "karma"
    print("  [PASS] Sanskrit word: karma -> 25 00 0c 0f 00 -> karma")


def test_word_encoding_ukrainian():
    u = UPC8()
    # сани = s + a + n + y
    encoded = u.encode_ukrainian_word("\u0441\u0430\u043d\u0438")
    assert len(encoded) == 4
    assert encoded[0] == 0x29
    assert encoded[2] == 0x12
    # джаз = dzh + a + z (3 bytes, дж is one code)
    encoded = u.encode_ukrainian_word("\u0434\u0436\u0430\u0437")
    assert len(encoded) == 3
    assert encoded[0] == 0x38
    # ць = single multi-char letter
    encoded = u.encode_ukrainian_word("\u0446\u044c")
    assert len(encoded) == 1
    assert encoded[0] == 0x46
    print("  [PASS] Ukrainian word encoding: multi-char letters (дж, ць, щ)")


def test_pratyahara_ac():
    u = UPC8()
    members = u.pratyahara("ac")
    assert len(members) == 9
    sounds = [u.decode(m).get("slp1", "?") for m in members]
    assert "a" in sounds and "E" in sounds and "O" in sounds
    assert "k" not in sounds
    print(f"  [PASS] Pratyahara 'ac' -> 9 vowels: {sounds}")


def test_pratyahara_hal():
    u = UPC8()
    members = u.pratyahara("hal")
    # 33 consonants: 34 listed consonant positions (h through sutra 14's l),
    # minus 1 for h's alias dedup (sutra 5 and 14 share code 0x09).
    # Was wrongly asserted as 32 before the marker/sound spelling-collision
    # fix -- 'l' is both sutra 6's listed sound and sutra 14's marker, and
    # the old code dropped every 'l' by spelling, not just the marker's.
    assert len(members) == 33, f"hal should have 33 members (h deduplicated, l included), got {len(members)}"
    sounds = [u.decode(m).get("slp1", "?") for m in members]
    assert "a" not in sounds
    assert "k" in sounds and "p" in sounds
    assert "S" in sounds and "z" in sounds and "s" in sounds
    assert "l" in sounds, "sutra 6's listed 'l' must be included, not dropped as if it were sutra 14's marker"
    # h should appear only once (alias deduplicated)
    assert sounds.count("h") == 1, f"h should appear once, got {sounds.count('h')}"
    print(f"  [PASS] Pratyahara 'hal' -> 33 consonants (h deduplicated, l included)")


def test_pratyahara_marker_sound_collisions():
    """Regression test for the marker/sound spelling-collision bug: a
    listed sound must not be dropped just because some OTHER sutra's
    marker happens to have the same SLP1 letter. Six known collision
    families, from independent review (Manus AI deep review + Sarvam
    cross-check against traditional grammar, both confirmed 2026-08-18):
    l/y/r/m/v/Y collide with markers of sutras 14/12/13/7/11/8."""
    u = UPC8()

    def sounds_of(notation):
        return [u.decode(c).get("slp1", "?") for c in u.pratyahara(notation)]

    # hal: marker 'l' (sutra 14) vs listed 'l' (sutra 6) -- covered above too
    assert "l" in sounds_of("hal")
    # ay: marker 'y' (sutra 12) vs listed 'y' (sutra 5)
    assert "y" in sounds_of("ay"), "listed 'y' (sutra 5) must survive despite sutra 12's marker also being 'y'"
    # ar: marker 'r' (sutra 13) vs listed 'r' (sutra 5)
    assert "r" in sounds_of("ar"), "listed 'r' (sutra 5) must survive despite sutra 13's marker also being 'r'"
    # am: marker 'm' (sutra 7) vs listed 'm' (sutra 7 itself)
    assert "m" in sounds_of("am"), "listed 'm' (sutra 7) must survive despite sutra 7's own marker also being 'm'"
    # aY: marker 'Y' (sutra 8) vs listed 'Y' (sutra 7)
    assert "Y" in sounds_of("aY"), "listed 'Y' (sutra 7) must survive despite sutra 8's marker also being 'Y'"
    # av: marker 'v' (sutra 11) vs listed 'v' (sutra 5)
    assert "v" in sounds_of("av"), "listed 'v' (sutra 5) must survive despite sutra 11's marker also being 'v'"
    print("  [PASS] All 6 marker/sound spelling-collision families resolved correctly (l/y/r/m/Y/v)")


def test_pratyahara_ik():
    u = UPC8()
    members = u.pratyahara("ik")
    assert len(members) == 4
    sounds = [u.decode(m).get("slp1", "?") for m in members]
    assert sounds == ["i", "u", "f", "x"]
    print(f"  [PASS] Pratyahara 'ik' -> 4 close vowels: {sounds}")


def test_pratyahara_Sar():
    u = UPC8()
    members = u.pratyahara("Sar")
    assert len(members) == 3
    sounds = [u.decode(m).get("slp1", "?") for m in members]
    assert sounds == ["S", "z", "s"]
    print(f"  [PASS] Pratyahara 'Sar' -> 3 sibilants: {sounds}")


def test_pratyahara_yaR():
    """yaR = semivowels. Marker R (N) appears in sutra 1 and sutra 6.
    Forward scan from y (sutra 5) should find sutra 6's R."""
    u = UPC8()
    members = u.pratyahara("yaR")
    assert len(members) == 4
    sounds = [u.decode(m).get("slp1", "?") for m in members]
    assert sounds == ["y", "v", "r", "l"]
    print(f"  [PASS] Pratyahara 'yaR' -> 4 semivowels: {sounds}")


def test_natural_classes():
    u = UPC8()
    assert u.is_vowel(0x00) and not u.is_consonant(0x00)
    assert u.is_vowel(0x01) and not u.is_consonant(0x01)
    assert u.is_consonant(0x09) and not u.is_vowel(0x09)
    assert u.is_consonant(0x25) and not u.is_vowel(0x25)
    assert u.is_stop(0x25) and u.is_stop(0x26) and u.is_stop(0x19)
    assert not u.is_stop(0x09)
    assert u.is_sibilant(0x27) and u.is_sibilant(0x28) and u.is_sibilant(0x29)
    assert not u.is_sibilant(0x25)
    assert u.is_semivowel(0x0A) and u.is_semivowel(0x0C)
    assert not u.is_semivowel(0x00)
    print("  [PASS] Natural class tests (vowel/consonant/stop/sibilant/semivowel)")


def test_code_space_stats():
    u = UPC8()
    s = u.stats()
    assert s["canonical"] == 42
    assert s["sanskrit_extended"] == 7
    assert s["ukrainian_shared"] == 13
    assert s["ukrainian_new"] == 31
    assert s["total_assigned"] == 80
    assert s["reserved"] == 176
    print(f"  [PASS] Code space: {s['total_assigned']} assigned, {s['reserved']} reserved")


def test_reserved_codes():
    u = UPC8()
    for code in [0x50, 0x7F, 0x80, 0xFE, 0xFF]:
        assert u.decode(code)["layer"] == "reserved"
    print("  [PASS] Reserved codes 0x50-0xFF are unassigned")


def test_roundtrip_sanskrit():
    u = UPC8()
    word = "karma"
    encoded = u.encode_sanskrit_word(word)
    decoded = u.decode_bytes(encoded)
    reconstructed = "".join(d.get("slp1", "?") for d in decoded)
    assert reconstructed == word
    print(f"  [PASS] Roundtrip: {word} -> {encoded.hex(' ')} -> {reconstructed}")


def test_roundtrip_ukrainian():
    u = UPC8()
    word = "\u0441\u0430\u043d\u0438"  # сани
    encoded = u.encode_ukrainian_word(word)
    assert len(encoded) == 4
    assert u.decode(encoded[0])["layer"] in ("canonical", "ukrainian_new")
    print(f"  [PASS] Roundtrip: {word} -> {encoded.hex(' ')}")


def test_unresolved_ipa_tracking():
    u = UPC8()
    info = u.decode(0x33)  # Ukrainian a
    assert info["ipa"] == "unresolved"
    assert len(info["ipa_candidates"]) > 0
    assert "a" in info["ipa_candidates"]
    info = u.decode(0x3B)  # Ukrainian sh
    assert info["ipa"] != "unresolved"
    print("  [PASS] Unresolved IPA tracking with candidates")


def test_h_alias():
    """h appears in sutra 5 and sutra 14; both map to same code 0x09."""
    u = UPC8()
    h_info = u.decode(0x09)
    assert h_info["slp1"] == "h"
    assert h_info["sutra"] == 5
    assert h_info.get("alias_sutras") == [14], f"alias_sutras should be [14], got {h_info.get('alias_sutras')}"
    # Encoding h should always give 0x09
    assert u.encode_sanskrit("h") == 0x09
    print("  [PASS] h alias: sutra 5 code 0x09, alias_sutras=[14]")


def test_code_space_no_gaps():
    """Canonical: 0x00-0x29 (42 codes), extended: 0x2A-0x30 (7), ukr: 0x31-0x4F (31)."""
    u = UPC8()
    # Check no gaps in canonical
    for code in range(0x00, 0x2A):
        assert code in u.table, f"Gap at 0x{code:02X} in canonical"
    for code in range(0x2A, 0x31):
        assert code in u.table, f"Gap at 0x{code:02X} in extended"
    for code in range(0x31, 0x50):
        assert code in u.table, f"Gap at 0x{code:02X} in ukrainian"
    # 0x50 should be reserved
    assert 0x50 not in u.table
    print("  [PASS] No gaps in code space: 0x00-0x4F fully assigned")


def run_all():
    print("=" * 60)
    print("UPC-8 Test Suite")
    print("=" * 60)

    tests = [
        ("Canon source provenance",     test_canon_source_provenance),
        ("Canon completeness",          test_canon_completeness),
        ("Canonical codes",             test_canonical_codes),
        ("Sanskrit extended",           test_sanskrit_extended),
        ("Ukrainian shared",            test_ukrainian_shared),
        ("Ukrainian new",               test_ukrainian_new),
        ("Word encoding (Sanskrit)",    test_word_encoding_sanskrit),
        ("Word encoding (Ukrainian)",   test_word_encoding_ukrainian),
        ("Pratyahara: ac",              test_pratyahara_ac),
        ("Pratyahara: hal",             test_pratyahara_hal),
        ("Pratyahara: marker/sound collisions", test_pratyahara_marker_sound_collisions),
        ("Pratyahara: ik",              test_pratyahara_ik),
        ("Pratyahara: Sar",             test_pratyahara_Sar),
        ("Pratyahara: yaR",             test_pratyahara_yaR),
        ("Natural classes",             test_natural_classes),
        ("Code space stats",            test_code_space_stats),
        ("Reserved codes",              test_reserved_codes),
        ("Roundtrip Sanskrit",          test_roundtrip_sanskrit),
        ("Roundtrip Ukrainian",         test_roundtrip_ukrainian),
        ("Unresolved IPA",              test_unresolved_ipa_tracking),
        ("h alias (sutra 5 & 14)",     test_h_alias),
        ("No gaps in code space",       test_code_space_no_gaps),
    ]

    passed = 0
    failed = 0
    for name, func in tests:
        try:
            func()
            passed += 1
        except Exception as e:
            print(f"  [FAIL] {name}: {e}")
            failed += 1

    print(f"\n{'=' * 60}")
    print(f"Results: {passed} passed, {failed} failed, {passed + failed} total")
    if failed == 0:
        print("ALL TESTS PASSED")
    else:
        print(f"{failed} TEST(S) FAILED")
    print("=" * 60)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(run_all())
