; prototype/fpga/gen_matrix.lisp
; Native my-lisp replacement core for prototype/fpga/gen_matrix.py.
;
; This first GREEN slice preserves the Python generator's semantic contract:
;   - input: existing SLP1 engineering projection of the immutable canon;
;   - index model: sound-id/42 ONLY (duplicate h aliases first h);
;   - 546 two-character pratyahara keys, lexicographically ordered;
;   - expansion behavior matches the legacy resolver, including the case where
;     a requested terminal marker occurred before the chosen start sound and
;     the resolver therefore runs to the end of the canon.
;
; File rendering (C/Verilog/MIF/Lisp) is deliberately a later slice after
; semantic parity is green. No hard-coded copy of the 14 sutras lives here.

(load "lib/canon/siva-sutras-index.lisp")

(def fpga-canon (read-siva-sutras-slp1))

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
  (lambda () (sound-ids/42 fpga-canon)))

(def matrix-sounds
  (lambda () (map cadr (matrix-sound-rows))))

(def matrix-sound-count
  (lambda () (length (matrix-sounds))))

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

(def make-matrix-entry
  (lambda (start marker)
    (let ((members (resolve-pratyahara start marker)))
      (list
        (string->symbol (string-append start marker))
        members
        (mask/sound-id-42 members fpga-canon)))))

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
