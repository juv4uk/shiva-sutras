"""Independent check of ksetra/astadhyayi/pratyahara-usage.yaml against the canon.

shiva-sutras#48. Every pratyahara entry is re-derived from `ksetra/canon/siva-sutras.yaml`
(the 14 sutras: sounds + one it-marker each) and compared with the `set` listed in the usage
file. Nothing here imports prototype/upc14*.

Rule (1.1.71 adir antyena sahetA): a pratyahara is a start sound plus an it-marker; it stands
for the start sound and every sound between it and the marker (the marker itself is not in it).

Which occurrence of a repeated marker is meant is not decided by the sutras. The Kasika
(kAshikAvRRitti.txt, lines 99-103, at the sutra `la N`) states the usage:
  * `iN` always uses the LATER N (the marker of `la N`, sutra 6);
  * `aN` uses the EARLIER N (sutra 1), except in 1.1.69 (`aNudit savarNasya cApratyayaH`),
    which uses the later one (the usage file records that as the separate entry `aN2`).
For every other id the marker is the first occurrence of that letter AFTER the start sound.
"""

import os
import unicodedata
import unittest

import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CANON = os.path.join(REPO_ROOT, "ksetra", "canon", "siva-sutras.yaml")
USAGE = os.path.join(REPO_ROOT, "ksetra", "astadhyayi", "pratyahara-usage.yaml")

# Explicit occurrence choices from the Kasika (1-based count among the markers of that letter).
NTH_MARKER = {"iṇ": 2, "aṇ2": 2, "aṇ": 1}


def nfc(text):
    return unicodedata.normalize("NFC", text)


def load_stream():
    """Return (sounds, markers): `sounds` = [(sutra_id, sound)], `markers` = [(sutra_id, marker)]."""
    with open(CANON, encoding="utf-8") as handle:
        canon = yaml.safe_load(handle)
    sounds, markers = [], []
    for sutra in canon["sutras"]:
        for sound in sutra["sounds"]:
            sounds.append((sutra["id"], nfc(sound)))
        markers.append((sutra["id"], nfc(sutra["it_marker_iast"])))
    return sounds, markers


def load_entries():
    with open(USAGE, encoding="utf-8") as handle:
        return yaml.safe_load(handle)["pratyaharas"]


def resolve(entry_id, sounds, markers):
    """Return the expected set of sounds for `entry_id`, or raise KeyError with the reason."""
    ident = nfc(entry_id).rstrip("0123456789")
    marker_letters = {m for _, m in markers}
    sound_letters = {s for _, s in sounds}
    marker = ident[-1]
    if marker not in marker_letters:
        raise KeyError(f"{entry_id}: last letter {marker!r} is not an it-marker of any sutra")
    start = ident[:-1]
    if start not in sound_letters:
        if start.endswith("a") and start[:-1] in sound_letters:
            start = start[:-1]                     # `ya`, `jha`, `kha` ...: the `a` is only for utterance
        else:
            raise KeyError(f"{entry_id}: start {start!r} is not a sound of the canon")
    first = next(i for i, (_, s) in enumerate(sounds) if s == start)
    start_sutra = sounds[first][0]
    candidates = [sutra for sutra, m in markers if m == marker]
    nth = NTH_MARKER.get(nfc(entry_id))
    if nth is not None:
        marker_sutra = candidates[nth - 1]
    else:
        later = [sutra for sutra in candidates if sutra > start_sutra]
        if not later:
            later = [sutra for sutra in candidates if sutra >= start_sutra]
        if not later:
            raise KeyError(f"{entry_id}: no marker {marker!r} after the start sound")
        marker_sutra = later[0]
    result = []
    for sutra, sound in sounds[first:]:
        if sutra > marker_sutra:
            break
        if sound not in result:
            result.append(sound)
    return result


class PratyaharaUsageAgainstCanon(unittest.TestCase):
    def setUp(self):
        self.sounds, self.markers = load_stream()
        self.entries = load_entries()

    def test_every_id_resolves_to_a_start_sound_and_an_it_marker(self):
        bad = []
        for entry in self.entries:
            try:
                resolve(entry["id"], self.sounds, self.markers)
            except KeyError as error:
                bad.append(str(error.args[0]))
        self.assertEqual(bad, [], "ids that are not (start sound + it-marker):\n" + "\n".join(bad))

    def test_every_set_is_the_interval_of_the_canon(self):
        wrong = []
        for entry in self.entries:
            try:
                want = resolve(entry["id"], self.sounds, self.markers)
            except KeyError:
                continue                            # reported by the test above
            have = []
            for sound in entry["set"]:
                if nfc(sound) not in have:
                    have.append(nfc(sound))
            if have != want:
                wrong.append(f"{entry['id']}: listed {len(have)} sounds {have}, canon gives {len(want)} {want}")
        self.assertEqual(wrong, [], "sets that differ from the canon:\n" + "\n".join(wrong))

    def test_ids_are_unique(self):
        ids = [nfc(entry["id"]) for entry in self.entries]
        self.assertEqual(len(ids), len(set(ids)))

    def test_the_three_entries_that_were_wrong(self):
        by_id = {nfc(entry["id"]): [nfc(s) for s in entry["set"]] for entry in self.entries}
        self.assertEqual(by_id.get("yaṇ"), ["y", "v", "r", "l"])
        self.assertEqual(by_id.get("jhaś"), ["jh", "bh", "gh", "ḍh", "dh", "j", "b", "g", "ḍ", "d"])
        self.assertEqual(by_id.get("haś"), ["h", "y", "v", "r", "l", "ñ", "m", "ṅ", "ṇ", "n",
                                             "jh", "bh", "gh", "ḍh", "dh", "j", "b", "g", "ḍ", "d"])
        self.assertEqual(by_id.get("bhaṣ"), ["bh", "gh", "ḍh", "dh"])
        self.assertEqual(by_id.get("ṅam"), ["ṅ", "ṇ", "n"])
        self.assertNotIn("bhaś", by_id)            # Kasika lists six s-sh pratyaharas: as haś vaś jaś jhaś baś
        self.assertNotIn("has", by_id)             # not a pratyahara: `s` is not an it-marker
        self.assertNotIn("jhas", by_id)


if __name__ == "__main__":
    unittest.main()
