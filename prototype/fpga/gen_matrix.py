#!/usr/bin/env python3
"""Pratyāhāra Membership Matrix Generator — complete self-contained script."""

siva_sutras = [
    ['a', 'i', 'u', 'R'],
    ['f', 'x', 'k'],
    ['e', 'o', 'N'],
    ['E', 'O', 'c'],
    ['h', 'y', 'v', 'r', 'w'],
    ['l', 'R'],
    ['Y', 'm', 'N', 'R', 'n', 'm'],
    ['J', 'B', 'Y'],
    ['G', 'Q', 'D', 'z'],
    ['j', 'b', 'g', 'q', 'd', 'S'],
    ['K', 'P', 'C', 'W', 'T', 'c', 'w', 't', 'v'],
    ['k', 'p', 'y'],
    ['S', 'z', 's', 'r'],
    ['h', 'l'],
]

# Extract sounds and it-markers
all_sounds = []
it_markers = []
for ss in siva_sutras:
    it_markers.append(ss[-1])
    for s in ss[:-1]:
        if s not in all_sounds:
            all_sounds.append(s)

sound_index = {s: i for i, s in enumerate(all_sounds)}

def resolve_pratyahara(adi, marker, sutras):
    result = []
    found = False
    for ss in sutras:
        sounds = ss[:-1]
        it = ss[-1]
        if not found:
            if adi in sounds:
                found = True
                idx = sounds.index(adi)
                if it == marker:
                    return sounds[idx:]
                else:
                    result = sounds[idx:]
        else:
            if it == marker:
                return result + sounds
            else:
                result = result + sounds
    return result

# Generate all valid pratyāhāras
all_pratyaharas = {}
for adi in all_sounds:
    for marker in set(it_markers):
        expansion = resolve_pratyahara(adi, marker, siva_sutras)
        if expansion and adi in expansion:
            key = f"{adi}{marker}"
            all_pratyaharas[key] = expansion

sorted_pa = sorted(all_pratyaharas.keys())

# Generate bitmasks
pa_bitmasks = {}
for pa_name in sorted_pa:
    expansion = all_pratyaharas[pa_name]
    mask = 0
    for s in expansion:
        mask |= (1 << sound_index[s])
    pa_bitmasks[pa_name] = mask

# === Generate MIF file ===
mif_lines = []
mif_lines.append("-- Pratyahara Membership Matrix - BRAM initialization data")
mif_lines.append("-- Generated from Siva Sutras (14 sutras, 42 sounds)")
mif_lines.append(f"-- {len(pa_bitmasks)} pratyaharas x 64-bit bitmask (42 bits used)")
mif_lines.append(f"-- Total: {len(pa_bitmasks) * 8} bytes")
mif_lines.append("DEPTH = %d;" % len(pa_bitmasks))
mif_lines.append("WIDTH = 64;")
mif_lines.append("ADDRESS_RADIX = HEX;")
mif_lines.append("DATA_RADIX = HEX;")
mif_lines.append("CONTENT BEGIN")
for i, pa_name in enumerate(sorted_pa):
    mask = pa_bitmasks[pa_name]
    mif_lines.append("  %03X : %016X;  -- %s" % (i, mask, pa_name))
mif_lines.append("END;")
mif_content = '\n'.join(mif_lines)

# === Generate C header ===
c_lines = []
c_lines.append("/* Pratyahara Membership Matrix - auto-generated */")
c_lines.append("/* %d pratyaharas x 64-bit bitmask */" % len(pa_bitmasks))
c_lines.append("/* %d sounds indexed 0-%d */" % (len(all_sounds), len(all_sounds)-1))
c_lines.append("")
c_lines.append("#define NUM_SOUNDS %d" % len(all_sounds))
c_lines.append("#define NUM_PRATYAHARAS %d" % len(pa_bitmasks))
c_lines.append("")
c_lines.append("static const char sound_names[NUM_SOUNDS] = {")
c_lines.append("  " + ', '.join("'%s'" % s for s in all_sounds))
c_lines.append("};")
c_lines.append("")
c_lines.append("static const char pa_names[NUM_PRATYAHARAS][3] = {")
for pa_name in sorted_pa:
    c_lines.append("  {'%s', '%s', 0}," % (pa_name[0], pa_name[1]))
c_lines.append("};")
c_lines.append("")
c_lines.append("static const uint64_t pa_matrix[NUM_PRATYAHARAS] = {")
for pa_name in sorted_pa:
    mask = pa_bitmasks[pa_name]
    c_lines.append("  0x%016XULL,  /* %s */" % (mask, pa_name))
c_lines.append("};")
c_content = '\n'.join(c_lines)

# === Generate Verilog module ===
v_lines = []
v_lines.append("// Pratyahara Membership Matrix - FPGA BRAM Module")
v_lines.append("// Auto-generated from Siva Sutras (14 sutras, 42 sounds)")
v_lines.append("// %d pratyaharas x 64-bit bitmask" % len(pa_bitmasks))
v_lines.append("// Total memory: %d bytes" % (len(pa_bitmasks) * 8))
v_lines.append("//")
v_lines.append("module pratyahara_matrix (")
v_lines.append("    input  wire        clk,")
v_lines.append("    input  wire [5:0]  sound_idx,   // 0-41")
v_lines.append("    input  wire [9:0]  pa_idx,      // 0-545")
v_lines.append("    output reg         is_member")
v_lines.append(");")
v_lines.append("")
v_lines.append("    reg [63:0] pa_rom [0:%d];" % (len(pa_bitmasks)-1))
v_lines.append("")
v_lines.append("    initial begin")
for i, pa_name in enumerate(sorted_pa):
    mask = pa_bitmasks[pa_name]
    v_lines.append("        pa_rom[%3d] = 64'h%016X;  // %s" % (i, mask, pa_name))
v_lines.append("    end")
v_lines.append("")
v_lines.append("    always @(posedge clk) begin")
v_lines.append("        is_member <= pa_rom[pa_idx][sound_idx];")
v_lines.append("    end")
v_lines.append("")
v_lines.append("endmodule")
v_content = '\n'.join(v_lines)

# === Generate my-lisp data ===
my_lines = []
my_lines.append(";; Pratyahara Membership Matrix - my-lisp data structure")
my_lines.append(";; Auto-generated from Siva Sutras (14 sutras, 42 sounds)")
my_lines.append(";; %d pratyaharas x 64-bit bitmask (42 bits used)" % len(pa_bitmasks))
my_lines.append(";;")
my_lines.append(";; Epistemic layer: ENGINEERING")
my_lines.append(";; Upstream: SS-CANON-001, SS-PRATYAHARA-001")
my_lines.append("")
my_lines.append("(def *sound-index*")
my_lines.append("  (quote (%s)))" % ' '.join(all_sounds))
my_lines.append("")
my_lines.append("(def *pa-names*")
my_lines.append("  (quote (%s)))" % ' '.join("(%s %s)" % (p[0], p[1]) for p in sorted_pa))
my_lines.append("")
my_lines.append(";; Membership: pa-matrix[i] = list of 42 bits")
my_lines.append("(def *pa-matrix*")
my_lines.append("  (quote (")
for pa_name in sorted_pa:
    mask = pa_bitmasks[pa_name]
    bits = ' '.join('1' if (mask >> j) & 1 else '0' for j in range(42))
    members = ', '.join(all_sounds[j] for j in range(42) if (mask >> j) & 1)
    my_lines.append("    (%s)  ; %s: %s" % (bits, pa_name, members))
my_lines.append("  )))")
my_lines.append("")
my_lines.append(";; Fast lookup: (nth sound-idx (nth pa-idx *pa-matrix*))")
my_lines.append("(def in-pratyahara-fast?")
my_lines.append("  (lambda (sound-idx pa-idx)")
my_lines.append("    (nth sound-idx (nth pa-idx *pa-matrix*))))")
my_content = '\n'.join(my_lines)

# === Save all files ===
import os
outdir = "/workspace/notes"
for name, content in [
    ("pratyahara_matrix.mif", mif_content),
    ("pratyahara_matrix.h", c_content),
    ("pratyahara_matrix.v", v_content),
    ("pratyahara_matrix.my", my_content),
]:
    path = os.path.join(outdir, name)
    with open(path, 'w') as f:
        f.write(content)
    print("  %s: %d bytes" % (name, len(content)))

# === Verification ===
print("\n=== Verification ===")
for name in ['ac', 'hl', 'ik', 'al', 'jS', 'JS', 'YR', 'ec', 'aR', 'ak']:
    mask = pa_bitmasks[name]
    members = [all_sounds[i] for i in range(42) if mask & (1 << i)]
    print("  %s: 0x%011X -> %s" % (name, mask, members))

print("\nTotal: %d sounds, %d pratyaharas, %d bytes ROM" % (
    len(all_sounds), len(pa_bitmasks), len(pa_bitmasks) * 8))
