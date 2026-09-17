; lib/canon/siva-sutras-index.lisp
; Explicit index models derived from the canon reader.
;
; BITMASK-INDEX-MODEL (#13):
;   canon-position/43 — every transmitted sound position is distinct;
;                       the repeated h in sutra 14 has its own position.
;   sound-id/42       — first-occurrence identity space for unique sounds;
;                       the repeated h aliases the earlier h.
;
; A bitmask is meaningless unless its index model is known. This file makes
; that distinction executable instead of relying on comments or convention.

(load "lib/canon/siva-sutras-reader.lisp")

(def index-row-sounds
  (lambda (row) (cdr (assoc (quote sounds) (cdr row)))))

(def enumerate-sounds-onto
  (lambda (sounds sutra-id local-index global-index acc)
    (cond
      ((atom sounds) (list global-index acc))
      (t
       (enumerate-sounds-onto
         (cdr sounds)
         sutra-id
         (+ local-index 1)
         (+ global-index 1)
         (cons
           (list
             global-index
             (car sounds)
             sutra-id
             local-index)
           acc))))))

(def canonical-positions-onto
  (lambda (rows global-index acc)
    (cond
      ((atom rows) (reverse acc))
      (t
       (let* ((row (car rows))
              (sutra-id (car row))
              (step (enumerate-sounds-onto
                      (index-row-sounds row)
                      sutra-id
                      0
                      global-index
                      acc)))
         (canonical-positions-onto
           (cdr rows)
           (car step)
           (cadr step)))))))

(def canonical-positions/43
  (lambda (canon)
    (canonical-positions-onto canon 0 (quote ()))))

(def sound-id-rows-onto
  (positions next-id seen acc)
    (cond
      ((atom positions) (reverse acc))
      (t
       (let* ((position (car positions))
              (position-index (car position))
              (sound (cadr position)))
         (cond
           ((member? sound seen)
            (sound-id-rows-onto (cdr positions) next-id seen acc))
           (t
            (sound-id-rows-onto
              (cdr positions)
              (+ next-id 1)
              (cons sound seen)
              (cons (list next-id sound position-index) acc))))))))

(def sound-ids/42
  (lambda (canon)
    (sound-id-rows-onto
      (canonical-positions/43 canon)
      0
      (quote ())
      (quote ()))))

(def index-of-sound
  (lambda (sound sound-id-rows)
    (cond
      ((atom sound-id-rows) (sound-id-not-found sound))
      ((equal? sound (cadr (car sound-id-rows))) (car (car sound-id-rows)))
      (t (index-of-sound sound (cdr sound-id-rows))))))

(def pow2
  (lambda (n)
    (cond
      ((eq n 0) 1)
      (t (* 2 (pow2 (- n 1)))))))

(def mask42-onto
  (sounds sound-id-rows seen acc)
    (cond
      ((atom sounds) acc)
      ((member? (car sounds) seen)
       (mask42-onto (cdr sounds) sound-id-rows seen acc))
      (t
       (mask42-onto
         (cdr sounds)
         sound-id-rows
         (cons (car sounds) seen)
         (+ acc (pow2 (index-of-sound (car sounds) sound-id-rows)))))))

(def mask/sound-id-42
  (lambda (sounds canon)
    (mask42-onto sounds (sound-ids/42 canon) (quote ()) 0)))

(def mask43-positions-onto
  (positions selected-sounds acc)
    (cond
      ((atom positions) acc)
      (t
       (let ((position (car positions)))
         (cond
           ((member? (cadr position) selected-sounds)
            (mask43-positions-onto
              (cdr positions)
              selected-sounds
              (+ acc (pow2 (car position)))))
           (t
            (mask43-positions-onto
              (cdr positions) selected-sounds acc)))))))

; This selects every canonical POSITION whose sound identity is in the set.
; Therefore a selected h sets both the sutra-5 and sutra-14 h positions.
(def mask/canon-position-43
  (lambda (sounds canon)
    (mask43-positions-onto
      (canonical-positions/43 canon)
      sounds
      0)))
