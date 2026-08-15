import os
import unittest
import yaml

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
SOURCES_DIR = os.path.join(REPO_ROOT, 'ksetra', 'astadhyayi', 'sources')
MANIFEST_FILE = os.path.join(REPO_ROOT, 'external_data', 'gretil_raw', 'manifest.json')


def source_files():
    return [os.path.join(SOURCES_DIR, f) for f in sorted(os.listdir(SOURCES_DIR)) if f.endswith('.yaml')]


class TestRealSourceInvariants(unittest.TestCase):

    def test_no_real_source_without_provenance(self):
        if not os.path.isdir(SOURCES_DIR):
            self.skipTest('sources dir not present')
        for path in source_files():
            with open(path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
            self.assertIsInstance(data, dict, f"{path}: expected a mapping")
            self.assertIn('source_id', data, f"{path}: missing source_id")
            self.assertIn('locator', data, f"{path}: missing locator")

    def test_real_sources_have_full_provenance(self):
        if not os.path.isdir(SOURCES_DIR):
            self.skipTest('sources dir not present')
        if not os.path.exists(MANIFEST_FILE):
            self.skipTest('GRETIL manifest not present (corpus gate not passed)')
        with open(MANIFEST_FILE, encoding='utf-8') as f:
            manifest = yaml.safe_load(f)
        manifest_sha = {m['filename']: m['sha256'] for m in manifest}

        for path in source_files():
            with open(path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
            prov = data.get('provenance', {})
            if prov.get('status') != 'REAL':
                continue
            self.assertIn('external_source', prov, f"{path}: REAL without external_source")
            self.assertIn('edition', prov, f"{path}: REAL without edition")
            self.assertIn('authenticity', prov, f"{path}: REAL without authenticity")
            self.assertIn('retrieved_at_utc', prov, f"{path}: REAL without retrieval timestamp")
            integrity = data.get('integrity', {})
            self.assertIn('source_file_sha256', integrity, f"{path}: REAL without source_file_sha256")
            self.assertIn('witness_text', data, f"{path}: REAL without witness_text")
            sutra = data['witness_text'].get('sutra', '')
            commentary = data['witness_text'].get('commentary', '')
            self.assertTrue(sutra or commentary, f"{path}: REAL with empty witness_text")

    def test_reproducible_sha256_matches_manifest(self):
        if not os.path.isdir(SOURCES_DIR) or not os.path.exists(MANIFEST_FILE):
            self.skipTest('corpus not present')
        with open(MANIFEST_FILE, encoding='utf-8') as f:
            manifest = yaml.safe_load(f)
        manifest_sha = {m['filename']: m['sha256'] for m in manifest}
        for path in source_files():
            with open(path, encoding='utf-8') as f:
                data = yaml.safe_load(f)
            integrity = data.get('integrity', {})
            fn = integrity.get('source_file')
            sha = integrity.get('source_file_sha256')
            if fn and sha:
                self.assertEqual(manifest_sha.get(fn), sha,
                                 f"{path}: sha256 not reproducible against manifest")

    def test_real_sources_contain_no_simulated_text(self):
        if not os.path.isdir(SOURCES_DIR):
            self.skipTest('sources dir not present')
        for path in source_files():
            with open(path, encoding='utf-8') as f:
                content = f.read()
            self.assertNotIn('Simulated Kasika raw text', content,
                             f"{path}: fabricated text found in REAL source")
            self.assertNotIn('Simulated Kasika raw text for', content,
                             f"{path}: fabricated text found in REAL source")
            data = yaml.safe_load(content)
            self.assertNotIn('raw_text', data,
                             f"{path}: legacy raw_text key must not replace witness_text")


if __name__ == '__main__':
    unittest.main()
