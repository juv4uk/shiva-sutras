; prototype/bitmask64/bitmask64.lisp
; Lisp-owned 42-sound mask semantics over exact non-negative integers.
;
; This is the correctness implementation for #19. Current my-lisp has no
; integer bitwise primitives, so set operations scan the fixed 42-bit domain
; arithmetically. Do NOT describe this path as one CPU instruction / O(1)
; word-bitwise execution. my-lisp#585 tracks the lower mechanism that can later
; accelerate the same observable API without moving domain meaning out of Lisp.

(load "lib/canon/pratyahara.lisp")

(def bitmask64-canon
  (read-siva-sutras-slp1))

(def bitmask64-sound-rows
  (sound-ids/42 bitmask64-canon))

(def bitmask64-sound-count
  (lambda () (length bitmask64-sound-rows)))

(def bitmask64-code-valid?
  (lambda (code)
    (and (>= code 0) (< code (bitmask64-sound-count)))))

(def bitmask64-find-sound-row
  (lambda (sound rows)
    (cond
      ((atom rows) (quote ()))
      ((equal? sound (cadr (car rows))) (car rows))
      (t (bitmask64-find-sound-row sound (cdr rows))))))

(def bitmask64-sound-index
  (lambda (sound)
    (let ((row (bitmask64-find-sound-row sound bitmask64-sound-rows)))
      (cond
        ((atom row) (bitmask64-unknown-sound sound))
        (t (car row))))))

(def bitmask64-sound-mask
  (lambda (sound-or-code)
    (cond
      ((string? sound-or-code)
       (pow2 (bitmask64-sound-index sound-or-code)))
      ((bitmask64-code-valid? sound-or-code)
       (pow2 sound-or-code))
      (t
       (bitmask64-code-out-of-range sound-or-code)))))

(def bitmask64-bit-present?
  (lambda (mask bit)
    (eq (mod (quotient mask (pow2 bit)) 2) 1)))

(def bitmask64-member?
  (lambda (sound-or-code mask)
    (cond
      ((string? sound-or-code)
       (let ((row
               (bitmask64-find-sound-row
                 sound-or-code
                 bitmask64-sound-rows)))
         (cond
           ((atom row) (quote ()))
           (t (bitmask64-bit-present? mask (car row))))))
      ((bitmask64-code-valid? sound-or-code)
       (bitmask64-bit-present? mask sound-or-code))
      (t (quote ())))))

(def bitmask64-combine-onto
  (lambda (mode m1 m2 bit acc)
    (cond
      ((eq bit (bitmask64-sound-count)) acc)
      (t
       (let* ((a (bitmask64-bit-present? m1 bit))
              (b (bitmask64-bit-present? m2 bit))
              (keep
                (cond
                  ((eq mode (quote union)) (or a b))
                  ((eq mode (quote intersect)) (and a b))
                  ((eq mode (quote diff)) (and a (not b)))
                  (t (bitmask64-unknown-combine-mode mode)))))
         (bitmask64-combine-onto
           mode
           m1
           m2
           (+ bit 1)
           (cond
             (keep (+ acc (pow2 bit)))
             (t acc))))))))

(def bitmask64-union
  (lambda (m1 m2)
    (bitmask64-combine-onto (quote union) m1 m2 0 0)))

(def bitmask64-intersect
  (lambda (m1 m2)
    (bitmask64-combine-onto (quote intersect) m1 m2 0 0)))

(def bitmask64-diff
  (lambda (m1 m2)
    (bitmask64-combine-onto (quote diff) m1 m2 0 0)))

(def bitmask64-subset?
  (lambda (m1 m2)
    (eq (bitmask64-diff m1 m2) 0)))

(def bitmask64-disjoint?
  (lambda (m1 m2)
    (eq (bitmask64-intersect m1 m2) 0)))

(def bitmask64-count-onto
  (lambda (mask bit acc)
    (cond
      ((eq bit (bitmask64-sound-count)) acc)
      (t
       (bitmask64-count-onto
         mask
         (+ bit 1)
         (cond
           ((bitmask64-bit-present? mask bit) (+ acc 1))
           (t acc)))))))

(def bitmask64-count
  (lambda (mask)
    (bitmask64-count-onto mask 0 0)))

(def bitmask64-mask-to-sounds
  (lambda (mask)
    (map
      cadr
      (filter
        (lambda (row)
          (bitmask64-bit-present? mask (car row)))
        bitmask64-sound-rows))))

(def bitmask64-sounds-to-mask-onto
  (lambda (sounds seen acc)
    (cond
      ((atom sounds) acc)
      ((member? (car sounds) seen)
       (bitmask64-sounds-to-mask-onto
         (cdr sounds) seen acc))
      (t
       (let ((row
               (bitmask64-find-sound-row
                 (car sounds)
                 bitmask64-sound-rows)))
         (bitmask64-sounds-to-mask-onto
           (cdr sounds)
           (cons (car sounds) seen)
           (cond
             ((atom row) acc)
             (t (+ acc (pow2 (car row)))))))))))

(def bitmask64-sounds-to-mask
  (lambda (sounds)
    (bitmask64-sounds-to-mask-onto
      sounds (quote ()) 0)))

; Explicit occurrence policy: callers cannot obtain a named range without
; choosing how repeated markers are interpreted.
(def bitmask64-pratyahara-mask/first-after-start
  (lambda (start marker)
    (mask/sound-id-42
      (resolve-pratyahara/first-after-start
        bitmask64-canon start marker)
      bitmask64-canon)))

(def bitmask64-pratyahara-mask/last-global
  (lambda (start marker)
    (mask/sound-id-42
      (resolve-pratyahara/last-global
        bitmask64-canon start marker)
      bitmask64-canon)))


; This exporter is independent of the disputed named-mask table and therefore
; can preserve the legacy target byte-for-byte safely.
(def bitmask64-export-verilog-lut
  (lambda ()
    (string-append
      "// Auto-generated synthesizable Verilog ROM/LUT for Pratyahara Membership\n"
      (string-append
        "module pratyahara_lut (\n"
        (string-append
          "    input  wire [5:0]  sound_code,    // 0x00 to 0x29 (6-bit code)\n"
          (string-append
            "    input  wire [63:0] pratyahara_mask,\n"
            (string-append
              "    output wire        is_member\n"
              (string-append
                ");\n"
                (string-append
                  "    assign is_member = pratyahara_mask[sound_code];\n"
                  "endmodule")))))))))
