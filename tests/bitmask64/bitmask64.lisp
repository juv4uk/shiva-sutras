; tests/bitmask64/bitmask64.lisp
; Correctness witnesses for the Lisp-owned 42-bit mask semantics.

(load "prototype/bitmask64/bitmask64.lisp")

(def require-equal
  (lambda (label actual expected)
    (cond
      ((equal? actual expected) (quote ok))
      (t (bitmask64-regression label actual expected)))))

(def require-true
  (lambda (label value)
    (cond
      (value (quote ok))
      (t (bitmask64-expected-true label value)))))

(def require-false
  (lambda (label value)
    (cond
      (value (bitmask64-expected-false label value))
      (t (quote ok)))))

; Canon-derived universe: 42 unique sound IDs, no local copied ordering.
(require-equal (quote sound-count) (bitmask64-sound-count) 42)
(require-equal (quote a-index) (bitmask64-sound-index "a") 0)
(require-equal (quote s-index) (bitmask64-sound-index "s") 41)
(require-equal (quote a-mask) (bitmask64-sound-mask "a") 1)
(require-equal (quote s-mask) (bitmask64-sound-mask "s") 2199023255552)

; Safe named witnesses are derived from explicit start+marker mechanics.
(def ac
  (bitmask64-pratyahara-mask/first-after-start "a" "c"))
(def hal
  (bitmask64-pratyahara-mask/first-after-start "h" "l"))
(def al
  (bitmask64-pratyahara-mask/first-after-start "a" "l"))
(def ik
  (bitmask64-pratyahara-mask/first-after-start "i" "k"))
(def ec
  (bitmask64-pratyahara-mask/first-after-start "e" "c"))
(def Sar
  (bitmask64-pratyahara-mask/first-after-start "S" "r"))
(def yaR
  (bitmask64-pratyahara-mask/first-after-start "y" "R"))

(require-equal (quote ac-mask) ac 511)
(require-equal (quote hal-count) (bitmask64-count hal) 33)
(require-equal (quote al-count) (bitmask64-count al) 42)
(require-equal (quote ik-mask) ik 30)
(require-equal (quote ec-mask) ec 480)
(require-equal (quote Sar-count) (bitmask64-count Sar) 3)
(require-equal (quote yaR-mask) yaR 15360)

; Legacy mechanism behavior preserved without bitwise host semantics.
(require-true (quote a-in-ac) (bitmask64-member? "a" ac))
(require-true (quote k-in-hal) (bitmask64-member? "k" hal))
(require-true (quote code-37-in-hal) (bitmask64-member? 37 hal))
(require-false (quote k-not-in-ac) (bitmask64-member? "k" ac))
(require-false (quote invalid-code-not-member) (bitmask64-member? 42 al))
(require-false
  (quote unknown-sound-not-member)
  (bitmask64-member? "?" al))
(require-equal
  (quote sounds-to-mask-ignores-unknown-legacy)
  (bitmask64-sounds-to-mask (quote ("a" "?" "i")))
  3)

(require-true (quote ac-hal-disjoint)
  (bitmask64-disjoint? ac hal))
(require-equal (quote ac-union-hal)
  (bitmask64-union ac hal)
  al)
(require-equal (quote al-minus-ac)
  (bitmask64-diff al ac)
  hal)
(require-equal (quote al-minus-hal)
  (bitmask64-diff al hal)
  ac)
(require-true (quote ik-subset-ac)
  (bitmask64-subset? ik ac))
(require-true (quote ec-subset-ac)
  (bitmask64-subset? ec ac))
(require-true (quote Sar-subset-hal)
  (bitmask64-subset? Sar hal))
(require-true (quote yaR-subset-hal)
  (bitmask64-subset? yaR hal))
(require-true (quote ik-ec-disjoint)
  (bitmask64-disjoint? ik ec))

(require-equal
  (quote roundtrip-ac)
  (bitmask64-sounds-to-mask (bitmask64-mask-to-sounds ac))
  ac)
(require-equal
  (quote roundtrip-al)
  (bitmask64-sounds-to-mask (bitmask64-mask-to-sounds al))
  al)

; #17 policy is now executable data, not hidden resolver convention.
(def aR-first
  (bitmask64-pratyahara-mask/first-after-start "a" "R"))
(def aR-last
  (bitmask64-pratyahara-mask/last-global "a" "R"))
(require-equal (quote aR-first-mask) aR-first 7)
(require-equal (quote aR-last-mask) aR-last 16383)
(require-false (quote repeated-marker-masks-diverge)
  (equal? aR-first aR-last))

(require-equal
  (quote verilog-export)
  (bitmask64-export-verilog-lut)
  "// Auto-generated synthesizable Verilog ROM/LUT for Pratyahara Membership\nmodule pratyahara_lut (\n    input  wire [5:0]  sound_code,    // 0x00 to 0x29 (6-bit code)\n    input  wire [63:0] pratyahara_mask,\n    output wire        is_member\n);\n    assign is_member = pratyahara_mask[sound_code];\nendmodule")

(print (quote bitmask64-lisp-correctness-green))
