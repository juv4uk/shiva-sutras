import os, sys, re, glob, json, hashlib
from indic_transliteration import sanscript

ROOT = "/home/agents/GitHub/shiva-sutras/ksetra"
SRC_DIR = f"{ROOT}/sanskritworld_texts"
TGT_DIR = f"{ROOT}/sanskritworld_texts_md"
MANIFEST_FILE = f"{TGT_DIR}/manifest.jsonl"
VERSION = "1.1.0"

# M1.1-corpus: deterministic genre tags derived from the source folder path.
# No semantic interpretation here — structural classification only.
GENRE_TAGS = {
    "vedic-literature/upanishad": "upaniṣad",
    "vedic-literature/samhita": "saṃhitā",
    "vedic-literature/brahmana": "brāhmaṇa",
    "vedic-literature/vedanga": "vedāṅga",
    "poetry/kavya": "kāvya",
    "poetry/nataka": "nāṭaka",
    "poetry/alankara": "alaṃkāra",
    "poetry/subhashita": "subhāṣita",
    "poetry/prosody": "chandas",
    "poetry/natyashastra": "nāṭyaśāstra",
    "poetry/narrative-literature": "kathā",
    "purana": "purāṇa",
    "epics": "itihāsa",
    "religious-literature/buddhist": "bauddha",
    "religious-literature/shaiva": "śaiva",
    "religious-literature/vaishnava": "vaiṣṇava",
    "religious-literature/ganapati": "gāṇapatya",
    "religious-literature/other-deities": "devatā",
    "shastra/grammar": "vyākaraṇa",
    "shastra/dharmashastra": "dharmaśāstra",
    "shastra/philosophy": "darśana",
    "shastra/ayurveda-alchemy-etc": "āyurveda",
    "shastra/astronomy-astrology-and-mathematics": "jyotiṣa-gaṇita",
    "shastra/kamashastra": "kāmaśāstra",
    "shastra/arthashastra": "arthaśāstra",
    "shastra/lexicography": "kośa",
    "researchpapers": "research",
    "unpublished-books": "unpublished",
}
TOP_FALLBACK = {
    "vedic-literature": "veda",
    "poetry": "sāhitya",
    "religious-literature": "dharma",
    "shastra": "śāstra",
}

def derive_tags(rel_path, status):
    """Deterministic structural tags: corpus + genre (from folder) +
    conversion state. Never semantic."""
    rel = rel_path.rsplit(".", 1)[0]
    tags = ["corpus"]
    genre = None
    for prefix, tag in sorted(GENRE_TAGS.items(), key=lambda kv: -len(kv[0])):
        if rel == prefix or rel.startswith(prefix + "/"):
            genre = tag
            break
    if genre:
        tags.append(genre)
    else:
        top = rel.split("/")[0]
        if top in TOP_FALLBACK:
            tags.append(TOP_FALLBACK[top])
    tags.append("conv-exact" if status == "CONFIRMED" else "conv-partial")
    return tags

# Create output dir
os.makedirs(TGT_DIR, exist_ok=True)

# 1. Validation (Golden Tests)
def convert_span(text):
    text = text.replace("ओं", "oṃ").replace("ॐ", "oṃ")
    return sanscript.transliterate(text, sanscript.DEVANAGARI, sanscript.IAST)

def process_line(line):
    parts = re.split(r'([\u0900-\u097F\u1CD0-\u1CFF\uA8E0-\uA8FF]+)', line)
    out = []
    for p in parts:
        if not p: continue
        if re.match(r'^[\u0900-\u097F\u1CD0-\u1CFF\uA8E0-\uA8FF]+$', p):
            out.append(convert_span(p))
        else:
            out.append(p)
    return "".join(out)

def run_golden_tests():
    tests = [
        ("तुल्यास्यप्रयर्नं", "tulyāsyaprayarnaṃ"),
        ("क + ् + ष", "ka +  + ṣa"),
        ("Ingalls, ed.", "Ingalls, ed."),
        ("ओं नमः", "oṃ namaḥ"),
        ("ॐ नमः", "oṃ namaḥ"),
        ("।िन्गल्ल्स्", "|ingalls"),
        ("0123", "0123"), # ascii digits preserved
        ("०१२३", "0123") # devanagari digits -> iast digits? wait, sanscript converts dev digits to ascii digits
    ]
    for src, expected in tests:
        res = process_line(src)
        if res != expected:
            print(f"GOLDEN TEST FAILED: {src} -> {res} (Expected: {expected})")
            sys.exit(1)
    print("GOLDEN TESTS PASS.")

run_golden_tests()

# 2. Manifest Loading
processed = {}
if os.path.exists(MANIFEST_FILE):
    with open(MANIFEST_FILE, "r") as f:
        for line in f:
            if not line.strip(): continue
            record = json.loads(line)
            processed[record["source"]] = record

# 3. File Processing
files = glob.glob(f"{SRC_DIR}/**/*.txt", recursive=True)
files.sort()

counts = {"CONFIRMED": 0, "PARTIAL": 0, "UNRESOLVED": 0, "BROKEN": 0, "SKIPPED": 0}

for i, f in enumerate(files):
    rel_path = f.replace(SRC_DIR + "/", "")
    
    with open(f, "rb") as byte_file:
        raw = byte_file.read()
        
    source_sha256 = hashlib.sha256(raw).hexdigest()
    
    # Resume check
    if rel_path in processed:
        rec = processed[rel_path]
        if rec["source_sha256"] == source_sha256 and rec["converter_version"] == VERSION and rec["status"] == "CONFIRMED":
            counts["SKIPPED"] += 1
            continue
            
    # Decoding strictly
    text = None
    enc_used = None
    if raw.startswith(b'\xef\xbb\xbf'):
        try:
            text = raw.decode('utf-8-sig', errors='strict')
            enc_used = 'utf-8-sig'
        except: pass
    elif raw.startswith(b'\xff\xfe'):
        try:
            text = raw.decode('utf-16le', errors='strict').lstrip('\ufeff')
            enc_used = 'utf-16le'
        except: pass
    
    if not text:
        try:
            text = raw.decode('utf-8', errors='strict')
            enc_used = 'utf-8'
        except:
            try:
                text = raw.decode('utf-16le', errors='strict')
                enc_used = 'utf-16le'
            except:
                counts["BROKEN"] += 1
                with open(MANIFEST_FILE, "a") as mf:
                    mf.write(json.dumps({"source": rel_path, "source_sha256": source_sha256, "status": "BROKEN", "converter_version": VERSION}) + "\n")
                continue

    # Determine status
    status = "CONFIRMED"
    if "ओं" in text or "ॐ" in text or "।ि" in text:
        status = "PARTIAL/UNRESOLVED"
        
    derived_lines = []
    for line in text.split('\n'):
        l = line.strip('\r\n')
        derived_lines.append(process_line(l))
        
    derived_body = "\n".join(derived_lines) + "\n"

    tags = derive_tags(rel_path, status)
    tags_yaml = "\n".join(f"  - {t}" for t in tags)
    yaml = f"""---
derived: true
source_file: "{rel_path}"
source_sha256: "{source_sha256}"
source_encoding: "{enc_used}"
source_script: "Devanagari"
target_transliteration: "IAST"
mapping_contract_version: "1.0"
converter_version: "{VERSION}"
conversion_status: "{"partial" if status != "CONFIRMED" else "exact"}"
textual_status: "{"unreviewed"}"
line_mapping: "1:1"
tags:
{tags_yaml}
---
"""
    full_content = yaml + derived_body
    derived_sha256 = hashlib.sha256(full_content.encode('utf-8')).hexdigest()
    
    # Atomic write
    tgt_path = f"{TGT_DIR}/{rel_path}".replace(".txt", ".md")
    os.makedirs(os.path.dirname(tgt_path), exist_ok=True)
    tmp_path = tgt_path + ".tmp"
    
    with open(tmp_path, "w", encoding="utf-8") as tf:
        tf.write(full_content)
        tf.flush()
        os.fsync(tf.fileno())
        
    os.replace(tmp_path, tgt_path)
    
    # Checkpoint
    rec = {
        "source": rel_path,
        "source_sha256": source_sha256,
        "derived": rel_path.replace(".txt", ".md"),
        "status": status,
        "converter_version": VERSION,
        "derived_sha256": derived_sha256
    }
    with open(MANIFEST_FILE, "a") as mf:
        mf.write(json.dumps(rec) + "\n")
        
    if status == "CONFIRMED":
        counts["CONFIRMED"] += 1
    else:
        counts["UNRESOLVED"] += 1
        
    if (i+1) % 50 == 0:
        print(f"Processed {i+1}/{len(files)}...")

print("DONE.")
print(counts)
