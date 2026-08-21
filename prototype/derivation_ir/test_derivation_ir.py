#!/usr/bin/env python3
"""
Unit and Integration Test Suite for Derivation IR Prototype.
"""

import sys
import unittest
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from derivation_cell import DerivationCell, DerivationStream, MorphemeTag, AnubandhaTag, SvaraLength
from paribhasha_resolver import PaniniRule, RuleClassification, RuleScope, ParibhashaResolver
from graph_engine import CanonicalDerivations, DerivationDAG
from proof_certificate import ProofCertificateGenerator, ProofCertificateVerifier


class TestDerivationCell(unittest.TestCase):
    """Tests for 32-bit DerivationCell packing, unpacking, and stream operations."""

    def test_cell_pack_unpack_roundtrip(self):
        cell = DerivationCell(
            phoneme="B",
            svara=SvaraLength.UDATTA | SvaraLength.DIRGHA,
            anubandha=AnubandhaTag.S_IT | AnubandhaTag.P_IT,
            morpheme=MorphemeTag.DHATU
        )
        u32 = cell.to_uint32()
        recovered = DerivationCell.from_uint32(u32)

        self.assertEqual(recovered.phoneme, "B")
        self.assertEqual(recovered.svara, SvaraLength.UDATTA | SvaraLength.DIRGHA)
        self.assertEqual(recovered.anubandha, AnubandhaTag.S_IT | AnubandhaTag.P_IT)
        self.assertEqual(recovered.morpheme, MorphemeTag.DHATU)
        self.assertEqual(recovered, cell)

    def test_stream_slp1_rendering(self):
        stream = DerivationStream.from_slp1("Bavati", morpheme=MorphemeTag.TIN)
        self.assertEqual(stream.surface_text, "Bavati")
        self.assertEqual(len(stream), 6)

        packed = stream.pack_uint32_list()
        self.assertEqual(len(packed), 6)
        unpacked = DerivationStream.unpack_uint32_list(packed)
        self.assertEqual(unpacked.surface_text, "Bavati")


class TestParibhashaResolver(unittest.TestCase):
    """Tests for 5-tier conflict resolution hierarchy."""

    def setUp(self):
        self.resolver = ParibhashaResolver()

    def test_tier1_apavada_over_utsarga(self):
        # 3.1.68 kartari śap (utsarga) vs 2.4.75 juhotyādibhyaḥ śluḥ (apavāda)
        r_utsarga = PaniniRule("3.1.68", "कर्तरि शप्", "kartari Sap", RuleClassification.VIDHI)
        r_apavada = PaniniRule("2.4.75", "जुहोत्यादिभ्यः श्लुः", "juhotyAdibhyaH SluH", RuleClassification.VIDHI, is_apavada_for="3.1.68")

        res = self.resolver.resolve_binary_conflict(r_utsarga, r_apavada)
        self.assertEqual(res.winning_principle, "apavada")
        self.assertEqual(res.selected_rule.sutra_id, "2.4.75")
        self.assertEqual(res.rejected_rule.sutra_id, "3.1.68")

    def test_tier2_nitya_over_anitya(self):
        r_anitya = PaniniRule("6.1.77", "इको यणचि", "iko yaRaci", RuleClassification.VIDHI, is_nitya=False)
        r_nitya = PaniniRule("6.1.101", "अकः सवर्णे दीर्घः", "akaH savarRe dIrGaH", RuleClassification.VIDHI, is_nitya=True)

        res = self.resolver.resolve_binary_conflict(r_anitya, r_nitya)
        self.assertEqual(res.winning_principle, "nitya")
        self.assertEqual(res.selected_rule.sutra_id, "6.1.101")

    def test_tier3_antaranga_over_bahiranga(self):
        r_bahiranga = PaniniRule("6.1.87", "आद्गुणः", "AdguRaH", RuleClassification.VIDHI, is_antaranga=False)
        r_antaranga = PaniniRule("7.3.84", "सार्वधातुकार्धधातुकयोः", "sArvaDAtukArDaDAtukayoH", RuleClassification.VIDHI, is_antaranga=True)

        res = self.resolver.resolve_binary_conflict(r_bahiranga, r_antaranga)
        self.assertEqual(res.winning_principle, "antaranga")
        self.assertEqual(res.selected_rule.sutra_id, "7.3.84")

    def test_tier4_para_over_purva(self):
        # In Sapta-adhyāyī, 1.4.2 selects later rule
        r_earlier = PaniniRule("3.1.68", "कर्तरि शप्", "kartari Sap", RuleClassification.VIDHI)
        r_later = PaniniRule("3.1.69", "दिवादिभ्यः श्यन्", "divAdibhyaH Syan", RuleClassification.VIDHI)

        res = self.resolver.resolve_binary_conflict(r_earlier, r_later)
        self.assertEqual(res.winning_principle, "para")
        self.assertEqual(res.selected_rule.sutra_id, "3.1.69")

    def test_tier5_asiddhatva_tripadi(self):
        # 8.2.1 Tripādī rule is invisible to Sapta-adhyāyī
        r_sapta = PaniniRule("6.1.78", "एचोऽयवायावः", "eco 'yavAyAvaH", RuleClassification.VIDHI)
        r_tripadi = PaniniRule("8.2.66", "ससजुषो रुः", "sasajuzo ruH", RuleClassification.VIDHI)

        res = self.resolver.resolve_binary_conflict(r_sapta, r_tripadi)
        self.assertEqual(res.winning_principle, "asiddhatva")
        self.assertEqual(res.selected_rule.sutra_id, "6.1.78")


class TestCanonicalDerivationsAndCertificates(unittest.TestCase):
    """Tests for end-to-end derivation of bhavati and dadāti with certificate verification."""

    def test_bhavati_derivation_pipeline(self):
        dag = CanonicalDerivations.derive_bhavati()
        self.assertEqual(dag.derivation_id, "drv:canonical:bhavati-v0.1")
        self.assertEqual(len(dag.states), 9)
        self.assertEqual(dag.states[-1].surface_form, "Bavati")

        # Generate JSON certificate & verify
        cert_dict = ProofCertificateGenerator.to_json_dict(dag)
        errors = ProofCertificateVerifier.verify(cert_dict)
        self.assertEqual(errors, [], f"Proof verification failed: {errors}")

        # S-expression serialization
        sexpr = ProofCertificateGenerator.to_sexpr_str(dag)
        self.assertIn("(derivation-proof (id drv:canonical:bhavati-v0.1)", sexpr)
        self.assertIn("(surface-form \"Bavati\")", sexpr)

    def test_dadati_derivation_pipeline(self):
        dag = CanonicalDerivations.derive_dadati()
        self.assertEqual(dag.derivation_id, "drv:canonical:dadati-v0.1")
        self.assertEqual(len(dag.states), 10)
        self.assertEqual(dag.states[-1].surface_form, "dadAti")

        # Generate JSON certificate & verify
        cert_dict = ProofCertificateGenerator.to_json_dict(dag)
        errors = ProofCertificateVerifier.verify(cert_dict)
        self.assertEqual(errors, [], f"Proof verification failed: {errors}")

        # S-expression serialization
        sexpr = ProofCertificateGenerator.to_sexpr_str(dag)
        self.assertIn("(derivation-proof (id drv:canonical:dadati-v0.1)", sexpr)
        self.assertIn("(surface-form \"dadAti\")", sexpr)


if __name__ == "__main__":
    unittest.main()
