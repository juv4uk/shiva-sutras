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

; Renderer parity is byte-exact against artifacts committed from gen_matrix.py.
; No normalization of whitespace/newlines is allowed here.
(print (quote checking-c-header-byte-parity))
(require-equal (quote c-header-byte-parity)
  (render-c-header matrix)
  (read-file "prototype/fpga/pratyahara_matrix.h"))
(print (quote checking-verilog-byte-parity))
(require-equal (quote verilog-byte-parity)
  (render-verilog matrix)
  (read-file "prototype/fpga/pratyahara_matrix.v"))

(print (quote fpga-matrix-parity-green))
