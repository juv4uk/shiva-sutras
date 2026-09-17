; tests/canon/siva-sutras-reader.lisp
; Native regression witness for lib/canon/siva-sutras-reader.lisp.
;
; Run from repository root with my-lisp-cli:
;   my-lisp-cli tests/canon/siva-sutras-reader.lisp

(load "lib/canon/siva-sutras-reader.lisp")

(def require-equal
  (lambda (label actual expected)
    (cond
      ((equal? actual expected) (quote ok))
      (t (siva-sutras-reader-regression-failed label actual expected)))))

(def row-sounds
  (lambda (row) (cdr (assoc (quote sounds) (cdr row)))))

(def row-marker
  (lambda (row) (cdr (assoc (quote it-marker) (cdr row)))))

(def unique-onto
  (lambda (items acc)
    (cond
      ((atom items) acc)
      ((member? (car items) acc) (unique-onto (cdr items) acc))
      (t (unique-onto (cdr items) (cons (car items) acc))))))

(def canon (read-siva-sutras-canon))
(def all-sounds (reduce append (quote ()) (map row-sounds canon)))
(def unique-sounds (unique-onto all-sounds (quote ())))

(require-equal (quote sutra-count) (length canon) 14)
(require-equal (quote sound-position-count) (length all-sounds) 43)
(require-equal (quote unique-sound-count) (length unique-sounds) 42)

(require-equal (quote sutra-1-sounds)
  (row-sounds (nth 0 canon))
  (quote ("a" "i" "u")))
(require-equal (quote sutra-1-marker)
  (row-marker (nth 0 canon))
  "ṇ")

(require-equal (quote sutra-7-sounds)
  (row-sounds (nth 6 canon))
  (quote ("ñ" "m" "ṅ" "ṇ" "n")))
(require-equal (quote sutra-7-marker)
  (row-marker (nth 6 canon))
  "m")

(require-equal (quote sutra-12-sounds)
  (row-sounds (nth 11 canon))
  (quote ("k" "p")))
(require-equal (quote sutra-12-marker)
  (row-marker (nth 11 canon))
  "y")

(require-equal (quote sutra-14-sounds)
  (row-sounds (nth 13 canon))
  (quote ("h")))
(require-equal (quote sutra-14-marker)
  (row-marker (nth 13 canon))
  "l")

(print (quote siva-sutras-reader-green))
