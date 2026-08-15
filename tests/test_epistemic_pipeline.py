import unittest
import yaml
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'experiments', 'blind_reconstruction')))
from validator_v2 import SemanticValidator

class TestEpistemicPipeline(unittest.TestCase):
    def setUp(self):
        self.validator = SemanticValidator()
        self.base_record = {
            "sutra_id": "1.1.1",
            "workflow_status": "RESOLVED",
            "claims": [
                {"type": "authenticity", "status": "VERIFIED"},
                {"type": "integrity", "reproducible": True, "sha256_match": True}
            ],
            "evidence_layer": {
                "source_status": "REAL",
                "source_url": "http://example.com/1.1.1",
                "raw_text": "वृद्धिरादैच् इति सूत्रम्।",
                "sha256": "dummy"
            },
            "expert_reconstruction": {
                "operation_type": "reconstructed",
                "sound_set_relevance": "KNOWN"
            },
            "uncertainty": {"type": "NONE"}
        }

    def validate_record(self, record):
        temp_path = "temp_test_record.yaml"
        with open(temp_path, "w", encoding="utf-8") as f:
            yaml.dump(record, f, allow_unicode=True)
        is_valid, messages = self.validator.validate_file(temp_path)
        if os.path.exists(temp_path):
            os.remove(temp_path)
        return is_valid, messages

    def test_reject_synthetic_provenance_with_valid_checksum(self):
        record = self.base_record
        record["claims"][0]["status"] = "AUTHENTICITY_UNVERIFIED"
        is_valid, msgs = self.validate_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any("Cannot resolve without VERIFIED authenticity" in m for m in msgs))

    def test_reject_real_status_with_boilerplate_text(self):
        record = self.base_record
        record["evidence_layer"]["raw_text"] = "वृद्धिरादैच् ... इति सूत्रम्।"
        is_valid, msgs = self.validate_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any("Ellipsis (...) found in evidence raw_text" in m for m in msgs))

    def test_reject_resolved_with_unknown_operation(self):
        record = self.base_record
        record["expert_reconstruction"]["operation_type"] = "insufficient_evidence"
        is_valid, msgs = self.validate_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any("RESOLVED requires reconstructed operation" in m for m in msgs))

    def test_reject_revealed_opaque_class(self):
        record = self.base_record
        record["expert_reconstruction"]["operands"] = [{"type": "focus", "role": "substituend", "value": "a, i, u"}]
        is_valid, msgs = self.validate_record(record)
        self.assertFalse(is_valid)
        self.assertTrue(any("Explicit phoneme lists are strictly forbidden" in m for m in msgs))

if __name__ == '__main__':
    unittest.main()
