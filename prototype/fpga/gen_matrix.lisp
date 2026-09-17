; prototype/fpga/gen_matrix.lisp
; Native my-lisp replacement core for prototype/fpga/gen_matrix.py.
;
; Preserves the Python generator's contract:
;   - input: existing SLP1 engineering projection of the immutable canon;
;   - index model: sound-id/42 ONLY (duplicate h aliases first h);
;   - 546 two-character pratyahara keys, lexicographically ordered;
;   - expansion behavior matches the legacy resolver;
;   - committed C and Verilog projections render byte-for-byte identically.
;
; No hard-coded copy of the 14 sutras lives here.

(load "lib/canon/siva-sutras-index.lisp")

(def fpga-canon (read-siva-sutras-slp1))
(def fpga-sound-id-rows (sound-ids/42 fpga-canon))
; Precompute the exact 42 sound-id bit values once. The previous version
; recomputed pow2 + linear ID lookup for every member of every one of the 546
; pratyahara rows; that was semantically correct but needlessly expensive.
(def fpga-sound-bit-rows
  (map
    (lambda (row) (list (cadr row) (pow2 (car row))))
    fpga-sound-id-rows))

(def fpga-row-sounds
  (lambda (row) (cdr (assoc (quote sounds) (cdr row)))))

(def fpga-row-marker
  (lambda (row) (cdr (assoc (quote it-marker) (cdr row)))))

(def unique-strings-onto
  (lambda (values seen acc)
    (cond
      ((atom values) (reverse acc))
      ((member? (car values) seen)
       (unique-strings-onto (cdr values) seen acc))
      (t
       (unique-strings-onto
         (cdr values)
         (cons (car values) seen)
         (cons (car values) acc))))))

(def unique-strings
  (lambda (values)
    (unique-strings-onto values (quote ()) (quote ()))))

(def insert-string
  (lambda (value sorted)
    (cond
      ((atom sorted) (list value))
      ((string<? value (car sorted)) (cons value sorted))
      (t (cons (car sorted) (insert-string value (cdr sorted)))))))

(def sort-strings-onto
  (lambda (remaining sorted)
    (cond
      ((atom remaining) sorted)
      (t (sort-strings-onto
           (cdr remaining)
           (insert-string (car remaining) sorted))))))

(def sort-strings
  (lambda (values) (sort-strings-onto values (quote ()))))

(def matrix-sound-rows
  (lambda () fpga-sound-id-rows))

(def matrix-sounds
  (lambda () (map cadr fpga-sound-id-rows)))

(def matrix-sound-count
  (lambda () (length fpga-sound-id-rows)))

(def matrix-markers
  (lambda ()
    (sort-strings
      (unique-strings (map fpga-row-marker fpga-canon)))))

(def drop-until-sound
  (lambda (sound sounds)
    (cond
      ((atom sounds) (quote ()))
      ((equal? sound (car sounds)) sounds)
      (t (drop-until-sound sound (cdr sounds))))))

(def resolve-pratyahara-onto
  (lambda (rows start marker started acc)
    (cond
      ((atom rows) acc)
      (t
       (let* ((row (car rows))
              (sounds (fpga-row-sounds row))
              (it-marker (fpga-row-marker row)))
         (cond
           (started
            (let ((next (append acc sounds)))
              (cond
                ((equal? it-marker marker) next)
                (t (resolve-pratyahara-onto
                     (cdr rows) start marker t next)))))
           (t
            (let ((from-start (drop-until-sound start sounds)))
              (cond
                ((atom from-start)
                 (resolve-pratyahara-onto
                   (cdr rows) start marker (quote ()) acc))
                ((equal? it-marker marker)
                 (append acc from-start))
                (t
                 (resolve-pratyahara-onto
                   (cdr rows) start marker t (append acc from-start))))))))))))

(def resolve-pratyahara
  (lambda (start marker)
    (resolve-pratyahara-onto
      fpga-canon start marker (quote ()) (quote ()))))

(def fpga-sound-bit
  (lambda (sound rows)
    (cond
      ((atom rows) (fpga-sound-bit-not-found sound))
      ((equal? sound (car (car rows))) (cadr (car rows)))
      (t (fpga-sound-bit sound (cdr rows))))))

(def mask42-cached-onto
  (lambda (members seen acc)
    (cond
      ((atom members) acc)
      ((member? (car members) seen)
       (mask42-cached-onto (cdr members) seen acc))
      (t
       (mask42-cached-onto
         (cdr members)
         (cons (car members) seen)
         (+ acc (fpga-sound-bit (car members) fpga-sound-bit-rows)))))))

(def mask42-cached
  (lambda (members)
    (mask42-cached-onto members (quote ()) 0)))

(def make-matrix-entry
  (lambda (start marker)
    (let ((members (resolve-pratyahara start marker)))
      (list
        (string->symbol (string-append start marker))
        members
        (mask42-cached members)))))

(def entries-for-sound
  (lambda (sound markers)
    (map (lambda (marker) (make-matrix-entry sound marker)) markers)))

(def build-pratyahara-matrix
  (lambda ()
    (let ((sounds (sort-strings (matrix-sounds)))
          (markers (matrix-markers)))
      (reduce
        append
        (quote ())
        (map (lambda (sound) (entries-for-sound sound markers)) sounds)))))

(def matrix-entry
  (lambda (name matrix)
    (assoc name matrix)))

(def matrix-members
  (lambda (name matrix)
    (cadr (matrix-entry name matrix))))

(def matrix-mask
  (lambda (name matrix)
    (third (matrix-entry name matrix))))

; ---------------------------------------------------------------------------
; Deterministic text rendering. These helpers deliberately avoid host format
; functions so the generated bytes belong to Lisp, not to Python/Rust printf.

; Balanced concatenation avoids rebuilding an ever-growing prefix for every
; line. This matters for the ~29 KiB generated C/Verilog projections in the
; interpreter, where a left-fold string append becomes quadratic.
(def merge-string-pairs-onto
  (lambda (parts acc)
    (cond
      ((atom parts) (reverse acc))
      ((atom (cdr parts)) (reverse (cons (car parts) acc)))
      (t
       (merge-string-pairs-onto
         (cddr parts)
         (cons (string-append (car parts) (cadr parts)) acc))))))

(def concat-strings
  (lambda (parts)
    (cond
      ((atom parts) "")
      ((atom (cdr parts)) (car parts))
      (t (concat-strings (merge-string-pairs-onto parts (quote ())))))))

(def intersperse-strings-onto
  (lambda (values separator first acc)
    (cond
      ((atom values) (reverse acc))
      (first
       (intersperse-strings-onto
         (cdr values) separator (quote ()) (cons (car values) acc)))
      (t
       (intersperse-strings-onto
         (cdr values)
         separator
         (quote ())
         (cons (car values) (cons separator acc)))))))

(def join-strings
  (lambda (values separator)
    (concat-strings
      (intersperse-strings-onto values separator t (quote ())))))

(def join-lines
  (lambda (lines) (join-strings lines "\n")))

(def hex-digits
  (quote ("0" "1" "2" "3" "4" "5" "6" "7"
          "8" "9" "A" "B" "C" "D" "E" "F")))

(def integer-hex-onto
  (lambda (n acc)
    (cond
      ((eq n 0) acc)
      (t
       (integer-hex-onto
         (quotient n 16)
         (string-append (nth (mod n 16) hex-digits) acc))))))

(def integer-hex
  (lambda (n)
    (cond
      ((eq n 0) "0")
      (t (integer-hex-onto n "")))))

(def pad-left
  (lambda (text width fill)
    (cond
      ((< (string-length text) width)
       (pad-left (string-append fill text) width fill))
      (t text))))

(def hex16
  (lambda (n) (pad-left (integer-hex n) 16 "0")))

(def decimal-width3
  (lambda (n) (pad-left (number->string n) 3 " ")))

(def entry-name-text
  (lambda (entry) (symbol->string (car entry))))

(def c-sound-token
  (lambda (sound) (concat-strings (list "'" sound "'"))))

(def c-name-line
  (lambda (entry)
    (let* ((name (entry-name-text entry))
           (a (string-first name))
           (m (string-first (string-rest name))))
      (concat-strings (list "  {'" a "', '" m "', 0},")))))

(def c-mask-line
  (lambda (entry)
    (concat-strings
      (list
        "  0x"
        (hex16 (third entry))
        "ULL,  /* "
        (entry-name-text entry)
        " */"))))

(def render-c-header
  (lambda (matrix)
    (let* ((sound-count (matrix-sound-count))
           (pa-count (length matrix))
           (sounds-line
             (concat-strings
               (list
                 "  "
                 (join-strings (map c-sound-token (matrix-sounds)) ", "))))
           (lines
             (append
               (list
                 "/* Pratyahara Membership Matrix - auto-generated */"
                 (concat-strings
                   (list "/* " (number->string pa-count) " pratyaharas x 64-bit bitmask */"))
                 (concat-strings
                   (list "/* " (number->string sound-count) " sounds indexed 0-"
                         (number->string (- sound-count 1)) " */"))
                 ""
                 (concat-strings (list "#define NUM_SOUNDS " (number->string sound-count)))
                 (concat-strings (list "#define NUM_PRATYAHARAS " (number->string pa-count)))
                 ""
                 "static const char sound_names[NUM_SOUNDS] = {"
                 sounds-line
                 "};"
                 ""
                 "static const char pa_names[NUM_PRATYAHARAS][3] = {")
               (append
                 (map c-name-line matrix)
                 (append
                   (list
                     "};"
                     ""
                     "static const uint64_t pa_matrix[NUM_PRATYAHARAS] = {")
                   (append (map c-mask-line matrix) (list "};")))))))
      (join-lines lines))))

(def verilog-rom-lines-onto
  (lambda (remaining index acc)
    (cond
      ((atom remaining) (reverse acc))
      (t
       (let ((entry (car remaining)))
         (verilog-rom-lines-onto
           (cdr remaining)
           (+ index 1)
           (cons
             (concat-strings
               (list
                 "        pa_rom["
                 (decimal-width3 index)
                 "] = 64'h"
                 (hex16 (third entry))
                 ";  // "
                 (entry-name-text entry)))
             acc)))))))

(def render-verilog
  (lambda (matrix)
    (let* ((pa-count (length matrix))
           (rom-lines (verilog-rom-lines-onto matrix 0 (quote ())))
           (lines
             (append
               (list
                 "// Pratyahara Membership Matrix - FPGA BRAM Module"
                 "// Auto-generated from Siva Sutras (14 sutras, 42 sounds)"
                 (concat-strings
                   (list "// " (number->string pa-count) " pratyaharas x 64-bit bitmask"))
                 (concat-strings
                   (list "// Total memory: " (number->string (* pa-count 8)) " bytes"))
                 "//"
                 "module pratyahara_matrix ("
                 "    input  wire        clk,"
                 "    input  wire [5:0]  sound_idx,   // 0-41"
                 (concat-strings
                   (list "    input  wire [9:0]  pa_idx,      // 0-"
                         (number->string (- pa-count 1))))
                 "    output reg         is_member"
                 ");"
                 ""
                 (concat-strings
                   (list "    reg [63:0] pa_rom [0:" (number->string (- pa-count 1)) "];"))
                 ""
                 "    initial begin")
               (append
                 rom-lines
                 (list
                   "    end"
                   ""
                   "    always @(posedge clk) begin"
                   "        is_member <= pa_rom[pa_idx][sound_idx];"
                   "    end"
                   ""
                   "endmodule")))))
      (join-lines lines))))
