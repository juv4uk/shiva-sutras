#!/usr/bin/env python3
"""Regression tests for canonical pratyāhāra ↔ UPC feature comparison.

The canonical member set always comes from ksetra/canon/siva-sutras.yaml via
probe.py.  UPC predicates are engineering views over the existing SA_FEATURES
registry and are never allowed to become a second authority.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from probe import compare_pratyahara_to_upc


def test_nyam_matches_nasal_feature_exactly():
    """ñam spans exactly the five canonical nasals in sūtra 7."""
    result = compare_pratyahara_to_upc("ñam", "nasal")

    assert result["status"] == "EXACT"
    assert result["canonical"] == ["ñ", "m", "ṅ", "ṇ", "n"]
    assert result["upc"] == ["ñ", "m", "ṅ", "ṇ", "n"]
    assert result["canonical_only"] == []
    assert result["upc_only"] == []


def test_jas_refuses_false_exact_without_aspiration_dimension():
    """Current SA_FEATURES collapses plain/aspirated voiced stops.

    Therefore jaś must not be advertised as one exact UPC predicate until the
    feature source actually contains an aspiration dimension.
    """
    result = compare_pratyahara_to_upc("jaś", "voiced-unaspirated-stop")

    assert result["status"] == "NOT_SINGLE_PREDICATE"
    assert result["canonical"] == ["j", "b", "g", "ḍ", "d"]
    assert result["upc"] is None
    assert "aspiration" in result["reason"].lower()


if __name__ == "__main__":
    test_nyam_matches_nasal_feature_exactly()
    test_jas_refuses_false_exact_without_aspiration_dimension()
    print("2/2 comparison tests passed")
