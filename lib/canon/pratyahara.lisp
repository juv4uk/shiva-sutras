; lib/canon/pratyahara.lisp
; Canon-derived pratyahara range mechanics with explicit repeated-marker policy.
;
; A start sound + marker glyph is not always a complete selector because the
; canonical marker ṇ (SLP1 R) occurs twice. Consumers must name their policy.

(load "lib/canon/siva-sutras-index.lisp")

(def pratyahara-row-sounds
  (lambda (row) (cdr (assoc (quote sounds) (cdr row)))))

(def pratyahara-row-marker
  (lambda (row) (cdr (assoc (quote it-marker) (cdr row)))))

(def pratyahara-drop-until-sound
  (lambda (sound sounds)
    (cond
      ((atom sounds) (quote ()))
      ((equal? sound (car sounds)) sounds)
      (t (pratyahara-drop-until-sound sound (cdr sounds))))))

; Legacy FPGA/generator policy: after the first start-sound occurrence, stop
; at the first row whose it-marker matches.
(def pratyahara-first-after-start-onto
  (lambda (rows start marker started acc)
    (cond
      ((atom rows) acc)
      (t
       (let* ((row (car rows))
              (sounds (pratyahara-row-sounds row))
              (it-marker (pratyahara-row-marker row)))
         (cond
           (started
            (let ((next (append acc sounds)))
              (cond
                ((equal? it-marker marker) next)
                (t
                 (pratyahara-first-after-start-onto
                   (cdr rows) start marker t next)))))
           (t
            (let ((from-start
                    (pratyahara-drop-until-sound start sounds)))
              (cond
                ((atom from-start)
                 (pratyahara-first-after-start-onto
                   (cdr rows) start marker (quote ()) acc))
                ((equal? it-marker marker) (append acc from-start))
                (t
                 (pratyahara-first-after-start-onto
                   (cdr rows)
                   start
                   marker
                   t
                   (append acc from-start))))))))))))

(def resolve-pratyahara/first-after-start
  (lambda (canon start marker)
    (pratyahara-first-after-start-onto
      canon start marker (quote ()) (quote ()))))

(def marker-end-positions-onto
  (lambda (rows next-index acc)
    (cond
      ((atom rows) (reverse acc))
      (t
       (let* ((row (car rows))
              (sounds (pratyahara-row-sounds row))
              (count (length sounds))
              (end-index (- (+ next-index count) 1)))
         (marker-end-positions-onto
           (cdr rows)
           (+ next-index count)
           (cons
             (list (pratyahara-row-marker row) end-index)
             acc)))))))

(def marker-end-positions
  (lambda (canon)
    (marker-end-positions-onto canon 0 (quote ()))))

(def last-marker-end
  (lambda (marker marker-ends)
    (let ((row (assoc marker (reverse marker-ends))))
      (cond
        ((atom row) (pratyahara-marker-not-found marker))
        (t (cadr row))))))

(def first-sound-position
  (lambda (sound positions)
    (cond
      ((atom positions) (pratyahara-start-not-found sound))
      ((equal? sound (cadr (car positions))) (car (car positions)))
      (t (first-sound-position sound (cdr positions))))))

(def sounds-between-positions
  (lambda (positions start-index end-index)
    (map
      cadr
      (filter
        (lambda (position)
          (and
            (>= (car position) start-index)
            (<= (car position) end-index)))
        positions))))

; Legacy UPC8 probe policy: Python dict overwrite made the last global
; occurrence of a repeated marker win. This is explicit here for migration
; parity; it is not declared the canonical linguistic interpretation.
(def resolve-pratyahara/last-global
  (lambda (canon start marker)
    (let* ((positions (canonical-positions/43 canon))
           (start-index (first-sound-position start positions))
           (end-index (last-marker-end marker (marker-end-positions canon))))
      (cond
        ((< end-index start-index) (quote ()))
        (t
         (sounds-between-positions
           positions start-index end-index))))))
