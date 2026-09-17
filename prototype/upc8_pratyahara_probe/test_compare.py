#!/usr/bin/env python3
"""Regression tests for canonical pratyāhāra ↔ UPC feature comparison.

The canonical member set always comes from ksetra/canon/siva-sutras.yaml via
probe.py. UPC predicates are engineering views over the existing SA_FEATURES
registry and are never allowed to become a second authority.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from probe import compare_pratyahara_to_upc


def test_nasal_pratyahara_matches_nasal_feature_exactly():
    """ñ + m spans exactly the five canonical nasals in sūtra 7."""
    result = compare_pratyahara_to_upc("ñm", "nasal")

    assert result["status"] == "EXACT"
    assert result["canonical"] == ["ñ", "m", "ṅ", "ṇ", "n"]
    assert result["upc"] == ["ñ", "m", "ṅ", "ṇ", "n"]
    assert result["canonical_only"] == []
    assert result["upc_only"] == []


def test_jas_refuses_false_exact_without_aspiration_dimension():
    """Current SA_FEATURES collapses plain/aspirated voiced stops.

    Therefore j + ś must not be advertised as one exact UPC predicate until
    the feature source actually contains an aspiration dimension.
    """
    result = compare_pratyahara_to_upc("jś", "voiced-unaspirated-stop")

    assert result["status"] == "NOT_SINGLE_PREDICATE"
    assert result["canonical"] == ["j", "b", "g", "ḍ", "d"]
    assert result["upc"] is None
    assert "aspiration" in result["reason"].lower()


def test_hal_matches_consonants_and_collapses_duplicate_h_position():
    """h + l spans all consonants; repeated canonical h is one set member."""
    result = compare_pratyahara_to_upc("hl", "consonant")

    assert result["status"] == "EXACT"
    assert len(result["canonical"]) == 33
    assert result["canonical"].count("h") == 1
    assert result["canonical"] == result["upc"]
    assert result["canonical_only"] == []
    assert result["upc_only"] == []


if __name__ == "__main__":
    test_nasal_pratyahara_matches_nasal_feature_exactly()
    test_jas_refuses_false_exact_without_aspiration_dimension()
    test_hal_matches_consonants_and_collapses_duplicate_h_position()
    print("3/3 comparison tests passed")
