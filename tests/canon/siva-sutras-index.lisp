; tests/canon/siva-sutras-index.lisp
; Regression for explicit 42-ID vs 43-position bitmask models.

(load "lib/canon/siva-sutras-index.lisp")

(def require-equal
  (lambda (label actual expected)
    (cond
      ((equal? actual expected) (quote ok))
      (t (siva-sutras-index-regression-failed label actual expected)))))

(def drop
  (lambda (n values)
    (cond
      ((eq n 0) values)
      (t (drop (- n 1) (cdr values))))))

(def canon (read-siva-sutras-slp1))
(def positions (canonical-positions/43 canon))
(def sound-ids (sound-ids/42 canon))
(def all-sounds (all-sounds-from-canon canon))
(def consonant-positions (drop 9 positions))
(def consonant-sounds (drop 9 all-sounds))
(def h-positions
  (filter (lambda (position) (equal? (cadr position) "h")) positions))

(require-equal (quote position-count) (length positions) 43)
(require-equal (quote unique-sound-id-count) (length sound-ids) 42)
(require-equal (quote repeated-h-position-count) (length h-positions) 2)
(require-equal (quote first-h-position) (car (car h-positions)) 9)
(require-equal (quote second-h-position) (car (cadr h-positions)) 42)
(require-equal (quote h-sound-id) (index-of-sound "h" sound-ids) 9)

; Full universes differ by exactly the repeated canonical h occurrence.
(require-equal (quote al-sound-id-42)
  (mask/sound-id-42 all-sounds canon)
  #x000003FFFFFFFFFF)
(require-equal (quote al-canon-position-43)
  (mask/canon-position-43 positions)
  #x000007FFFFFFFFFF)

; hal follows the same distinction: 33 unique consonant identities versus
; 34 canonical consonant positions because h occurs in sutra 5 and 14.
(require-equal (quote hal-unique-consonant-count)
  (length (sound-ids/42
            (drop 4 canon)))
  33)
(require-equal (quote hal-sound-id-42)
  (mask/sound-id-42 consonant-sounds canon)
  #x000003FFFFFFFE00)
(require-equal (quote hal-canon-position-43)
  (mask/canon-position-43 consonant-positions)
  #x000007FFFFFFFE00)

(print (quote siva-sutras-index-green))
