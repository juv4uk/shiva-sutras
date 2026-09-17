; tests/fpga/gen-matrix.lisp
; Differential-parity contract for replacing prototype/fpga/gen_matrix.py.

(load "prototype/fpga/gen_matrix.lisp")

(def require-equal
  (lambda (label actual expected)
    (cond
      ((equal? actual expected) (quote ok))
      (t
       (print label)
       (print (list (quote actual-length)
                    (cond ((string? actual) (string-length actual)) (t (quote n/a)))))
       (print (list (quote expected-length)
                    (cond ((string? expected) (string-length expected)) (t (quote n/a)))))
       (print (list (quote actual-sha256)
                    (cond ((string? actual) (sha256-hex actual)) (t (quote n/a)))))
       (print (list (quote expected-sha256)
                    (cond ((string? expected) (sha256-hex expected)) (t (quote n/a)))))
       (fpga-matrix-regression-failed label actual expected)))))

(def matrix (build-pratyahara-matrix))

(require-equal (quote sound-count) (matrix-sound-count) 42)
(require-equal (quote pratyahara-count) (length matrix) 546)

; Exact witnesses captured from the existing Python generator/committed matrix.
(require-equal (quote ac-mask) (matrix-mask (quote ac) matrix) 511)
(require-equal (quote hl-mask) (matrix-mask (quote hl) matrix) 4398046510592)
(require-equal (quote ik-mask) (matrix-mask (quote ik) matrix) 30)
(require-equal (quote al-mask) (matrix-mask (quote al) matrix) 4398046511103)
(require-equal (quote jS-mask) (matrix-mask (quote jS) matrix) 520093696)
(require-equal (quote JS-mask) (matrix-mask (quote JS) matrix) 536346624)
(require-equal (quote YR-mask) (matrix-mask (quote YR) matrix) 4398046495232)
(require-equal (quote ec-mask) (matrix-mask (quote ec) matrix) 480)
(require-equal (quote aR-mask) (matrix-mask (quote aR) matrix) 7)
(require-equal (quote ak-mask) (matrix-mask (quote ak) matrix) 31)

(require-equal (quote ac-members)
  (matrix-members (quote ac) matrix)
  (quote ("a" "i" "u" "f" "x" "e" "o" "E" "O")))

; hl contains both canonical h occurrences in its expansion, while its 42-ID
; mask aliases them to the same bit. This is the legacy Python contract.
(require-equal (quote hl-expansion-length)
  (length (matrix-members (quote hl) matrix))
  34)
(require-equal (quote hl-first)
  (car (matrix-members (quote hl) matrix))
  "h")
(require-equal (quote hl-last)
  (car (reverse (matrix-members (quote hl) matrix)))
  "h")

; The old Python generator was retired only after run #14 proved byte-for-byte
; differential parity for all four outputs. These pinned lengths + SHA-256
; values are that proven legacy contract, now checked without Python.
;
; Exercise the production writer ONCE, then hash the bytes it actually wrote.
; This avoids rendering all four large outputs twice inside the interpreted
; test while giving a stronger end-to-end writer witness.
(write-pratyahara-artifacts matrix "/workspace/notes")

(def mif-output (read-file "/workspace/notes/pratyahara_matrix.mif"))
(def c-header-output (read-file "/workspace/notes/pratyahara_matrix.h"))
(def verilog-output (read-file "/workspace/notes/pratyahara_matrix.v"))
(def lisp-data-output (read-file "/workspace/notes/pratyahara_matrix.my"))

(require-equal (quote mif-length) (string-length mif-output) 18284)
(require-equal (quote mif-sha256)
  (sha256-hex mif-output)
  "c6b78e19acf2d258fd22bbaf645d340890503aa7ed7dea574920aee594e42fc7")

(require-equal (quote c-header-length) (string-length c-header-output) 28935)
(require-equal (quote c-header-sha256)
  (sha256-hex c-header-output)
  "f3fb5c874d1fce207c50cb950a4973a44697aa8eda81320e18eb12233dea735f")

(require-equal (quote verilog-length) (string-length verilog-output) 28360)
(require-equal (quote verilog-sha256)
  (sha256-hex verilog-output)
  "e1a25ecba0a1410452d2a912476cbb3388d7e14ee6057000f267d2928468a900")

(require-equal (quote lisp-data-length) (string-length lisp-data-output) 81791)
(require-equal (quote lisp-data-sha256)
  (sha256-hex lisp-data-output)
  "188d7da12cbc3b513060a08be24b3ea6698ed6041e860fec3b676d27d4a1af2d")

(print (quote fpga-matrix-native-generator-green))
