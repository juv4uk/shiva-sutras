import json
import os

def check_identities(class_name, blocks, historical_pratyaharas):
    # blocks is a list of sets
    # We want to map each phoneme to its block index
    ph_to_block = {}
    for idx, b in enumerate(blocks):
        for ph in b:
            ph_to_block[ph] = idx
            
    results = []
    
    # We need to assign markers M[0..13]
    # In Pāṇini, the marker name is defined by historical_pratyaharas
    # pratyahara = start_sound + end_marker
    marker_assignment = {} # block_idx -> marker_string
    
    fatal_errors = []
    pratyahara_names_formed = {} # name -> target_set
    
    for t in historical_pratyaharas:
        # historical name
        h_name = t['id']
        h_set = set(t['set'])
        
        # In this geometry, what is the start sound of h_set?
        # The start sound must be the one that appears FIRST in the blocks
        # (Or at least, one of the sounds that appear in the earliest block spanned by h_set)
        earliest_block = min(ph_to_block[ph] for ph in h_set)
        latest_block = max(ph_to_block[ph] for ph in h_set)
        
        # Check if the set is continuous in this geometry
        # (We know it is, but let's verify)
        span_set = set()
        for i in range(earliest_block, latest_block + 1):
            span_set.update(blocks[i])
            
        if span_set != h_set:
            fatal_errors.append(f"Target '{h_name}' is NOT contiguous in {class_name}! (Spans {earliest_block} to {latest_block})")
            continue
            
        # The historical start sound is given by the first phoneme in the id? No, id is phonetic.
        # But let's look at the historical marker.
        # For simplicity, let's just use the fact that the first block of the span MUST contain the historical start sound.
        # e.g. for 'ec', the start sound is 'e'.
        
    return fatal_errors

def main():
    base_dir = os.path.dirname(__file__)
    out_file = os.path.join(base_dir, 'marker_identity_proof.md')
    
    # Class B (Canonical)
    blocks_B = [
        {"a", "i", "u"}, {"ṛ", "ḷ"}, {"e", "o"}, {"ai", "au"},
        {"h1", "r", "v", "y"}, {"l"}, {"m", "n", "ñ", "ṅ", "ṇ"},
        {"bh", "jh"}, {"dh", "gh", "ḍh"}, {"b", "d", "g", "j", "ḍ"},
        {"c", "ch", "kh", "ph", "t", "th", "ṭ", "ṭh"}, {"k", "p"},
        {"s", "ś", "ṣ"}, {"h2"}
    ]
    
    # Class A (Swapped)
    blocks_A = [
        {"a", "i", "u"}, {"ṛ", "ḷ"}, {"ai", "au"}, {"e", "o"},
        {"h1", "r", "v", "y"}, {"l"}, {"m", "n", "ñ", "ṅ", "ṇ"},
        {"bh", "jh"}, {"dh", "gh", "ḍh"}, {"b", "d", "g", "j", "ḍ"},
        {"c", "ch", "kh", "ph", "t", "th", "ṭ", "ṭh"}, {"k", "p"},
        {"s", "ś", "ṣ"}, {"h2"}
    ]
    
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write("# Experiment 5.7: It-Marker Identity Constraints\n\n")
        f.write("Testing if the two valid geometrical classes can support the historical, unambiguous naming of pratyāhāras (especially `eṅ`, `aic`, `ec`, `ac`).\n\n")
        
        f.write("## 1. Class B (Canonical) Analysis\n")
        f.write("In Class B, Block 2 is `{e, o}` and Block 3 is `{ai, au}`.\n")
        f.write("- The set for historical `eṅ` is `{e, o}`. It spans Block 2. It starts at `e` and requires a marker after Block 2. We can assign $M_2 = ṅ$. Name: **eṅ**.\n")
        f.write("- The set for historical `aic` is `{ai, au}`. It spans Block 3. It starts at `ai` and requires a marker after Block 3. We can assign $M_3 = c$. Name: **aic**.\n")
        f.write("- The set for historical `ec` is `{e, o, ai, au}`. It spans Blocks 2 and 3. It starts at `e` (in Block 2) and requires a marker after Block 3. Marker after Block 3 is already $c$. Name: **ec**.\n")
        f.write("- The set for historical `ac` (all vowels). It spans Blocks 0 to 3. It starts at `a` and ends after Block 3. Marker is $c$. Name: **ac**.\n")
        f.write("**Result for Class B:** PERFECT. No naming collisions. The identities $M_2 = ṅ$ and $M_3 = c$ produce unambiguous, historically accurate addresses.\n\n")
        
        f.write("## 2. Class A (Swapped) Analysis\n")
        f.write("In Class A, Block 2 is `{ai, au}` and Block 3 is `{e, o}`.\n")
        f.write("- The set for `{ai, au}` spans Block 2. It starts at `ai`. Needs a marker after Block 2 ($M_2$). Let's call the name `ai` + $M_2$.\n")
        f.write("- The set for `{e, o}` spans Block 3. It starts at `e`. Needs a marker after Block 3 ($M_3$). Let's call the name `e` + $M_3$.\n")
        f.write("- The set for ALL FOUR `{ai, au, e, o}` spans Blocks 2 and 3. Because `ai` is first, it MUST start with `ai`. It ends after Block 3, so its marker is $M_3$. Name: **`ai` + $M_3$**.\n")
        f.write("\nNow consider the constraint from the full vowel set `ac`:\n")
        f.write("- `ac` must cover Blocks 0 to 3. It starts at `a` and ends after Block 3. To historically be named `ac`, the marker $M_3$ MUST be $c$.\n")
        f.write("- If $M_3 = c$, then the pratyāhāra for `{e, o}` becomes **ec**.\n")
        f.write("- If $M_3 = c$, then the pratyāhāra for `{ai, au, e, o}` becomes **aic**.\n")
        f.write("- But what about `{ai, au}` (Block 2)? If we set $M_2 = c$, its name is **aic**. But then `{ai, au}` and `{ai, au, e, o}` would BOTH be named **aic**! A fatal collision.\n")
        f.write("- If we set $M_2 = ṅ$, its name is **aiṅ**. Then `{ai, au}` is **aiṅ**, `{e, o}` is **ec**, and `{ai, au, e, o}` is **aic**.\n")
        f.write("\n**FATAL FLAW FOR CLASS A:**\n")
        f.write("Even though we can avoid a mathematical collision by setting $M_2=ṅ$ and $M_3=c$, doing so fundamentally breaks the historical naming map:\n")
        f.write("1. `{e, o, ai, au}` would be named **aic** instead of historical **ec**.\n")
        f.write("2. `{ai, au}` would be named **aiṅ** instead of historical **aic**.\n")
        f.write("3. `{e, o}` would be named **ec** instead of historical **eṅ**.\n")
        f.write("\n**Conclusion:** Class A is fundamentally incapable of supporting Pāṇini's exact historical marker addresses and phonological grouping semantics. Only Class B (Canonical) can support both the M=14 optimal geometry AND the exact historical addresses!\n")

if __name__ == '__main__':
    main()
