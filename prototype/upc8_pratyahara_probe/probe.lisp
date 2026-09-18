; prototype/upc8_pratyahara_probe/probe.lisp
; Native my-lisp migration of probe.py.
;
; Migration rule: preserve the engineering prototype exactly. Feature values,
; weights, tie order, last-global repeated-marker policy, and report wording are
; legacy M0 data here; this file does not strengthen any linguistic claim.

(load "lib/canon/pratyahara.lisp")

; Feature row: (sound place manner voiced soft)
; Order is semantically relevant for legacy nearest-neighbour tie-breaking.
(def probe-sa-features
  (quote (
    ("a" 4 5 1 0) ("ā" 4 5 1 0)
    ("i" 3 5 1 0) ("ī" 3 5 1 0)
    ("u" 4 5 1 0) ("ū" 4 5 1 0)
    ("ṛ" 6 5 1 0) ("ḷ" 1 5 1 0)
    ("e" 3 5 1 0) ("ai" 3 5 1 0)
    ("o" 4 5 1 0) ("au" 4 5 1 0)
    ("k" 4 0 0 0) ("kh" 4 0 0 0)
    ("g" 4 0 1 0) ("gh" 4 0 1 0) ("ṅ" 4 3 1 0)
    ("c" 3 1 0 0) ("ch" 3 1 0 0)
    ("j" 3 1 1 0) ("jh" 3 1 1 0) ("ñ" 3 3 1 0)
    ("ṭ" 6 0 0 0) ("ṭh" 6 0 0 0)
    ("ḍ" 6 0 1 0) ("ḍh" 6 0 1 0) ("ṇ" 6 3 1 0)
    ("t" 1 0 0 0) ("th" 1 0 0 0)
    ("d" 1 0 1 0) ("dh" 1 0 1 0) ("n" 1 3 1 0)
    ("p" 0 0 0 0) ("ph" 0 0 0 0)
    ("b" 0 0 1 0) ("bh" 0 0 1 0) ("m" 0 3 1 0)
    ("y" 3 4 1 0) ("r" 2 4 1 0) ("l" 1 4 1 0) ("v" 0 4 1 0)
    ("ś" 3 2 0 0) ("ṣ" 6 2 0 0) ("s" 1 2 0 0) ("h" 5 2 1 0)
  )))

; Ukrainian row: (phoneme place manner voiced soft)
(def probe-uk-features
  (quote (
    ("б" 0 0 1 0)
    ("п" 0 0 0 0)
    ("д" 1 0 1 0)
    ("т" 1 0 0 0)
    ("ґ" 4 0 1 0)
    ("г" 5 2 1 0)
    ("й" 3 4 1 1)
    ("в" 0 4 1 0)
    ("м" 0 3 1 0)
    ("н" 1 3 1 0)
    ("і" 3 5 1 1)
    ("и" 3 5 1 0)
    ("ч" 3 1 0 1)
    ("ж" 2 2 1 0)
  )))

(def probe-abs
  (lambda (n) (cond ((< n 0) (- 0 n)) (t n))))

; Exact half-unit distance = legacy floating distance * 2:
;   place 4, manner 4, voiced 2, soft 1.
(def probe-distance2
  (lambda (a b)
    (+
      (* 4 (probe-abs (- (cadr a) (cadr b))))
      (* 4 (probe-abs (- (third a) (third b))))
      (* 2 (probe-abs (- (fourth a) (fourth b))))
      (probe-abs (- (fifth a) (fifth b))))))

(def probe-nearest-onto
  (lambda (uk remaining best-row best-distance)
    (cond
      ((atom remaining) (list (car best-row) best-distance))
      (t
       (let* ((candidate (car remaining))
              (distance (probe-distance2 uk candidate)))
         (cond
           ((< distance best-distance)
            (probe-nearest-onto
              uk (cdr remaining) candidate distance))
           (t
            (probe-nearest-onto
              uk (cdr remaining) best-row best-distance))))))))

(def probe-nearest
  (lambda (uk)
    (let* ((first (car probe-sa-features))
           (distance (probe-distance2 uk first)))
      (probe-nearest-onto
        uk (cdr probe-sa-features) first distance))))

(def probe-unique-onto
  (lambda (remaining seen acc)
    (cond
      ((atom remaining) (reverse acc))
      ((member? (car remaining) seen)
       (probe-unique-onto (cdr remaining) seen acc))
      (t
       (probe-unique-onto
         (cdr remaining)
         (cons (car remaining) seen)
         (cons (car remaining) acc))))))

(def probe-unique
  (lambda (values)
    (probe-unique-onto values (quote ()) (quote ()))))

(def probe-insert-string
  (lambda (value sorted)
    (cond
      ((atom sorted) (list value))
      ((string<? value (car sorted)) (cons value sorted))
      (t (cons (car sorted) (probe-insert-string value (cdr sorted)))))))

(def probe-sort-strings-onto
  (lambda (remaining sorted)
    (cond
      ((atom remaining) sorted)
      (t
       (probe-sort-strings-onto
         (cdr remaining)
         (probe-insert-string (car remaining) sorted))))))

(def probe-sort-strings
  (lambda (values)
    (probe-sort-strings-onto values (quote ()))))

(def probe-take-onto
  (lambda (remaining n acc)
    (cond
      ((atom remaining) (reverse acc))
      ((eq n 0) (reverse acc))
      (t (probe-take-onto (cdr remaining) (- n 1) (cons (car remaining) acc))))))

(def probe-take
  (lambda (values n)
    (probe-take-onto values n (quote ()))))

(def probe-join-onto
  (lambda (remaining separator first acc)
    (cond
      ((atom remaining) acc)
      (first
       (probe-join-onto
         (cdr remaining) separator (quote ()) (car remaining)))
      (t
       (probe-join-onto
         (cdr remaining)
         separator
         (quote ())
         (string-append acc (string-append separator (car remaining))))))))

(def probe-join
  (lambda (values separator)
    (probe-join-onto values separator t "")))

(def probe-pad-left
  (lambda (text width)
    (cond
      ((< (string-length text) width)
       (probe-pad-left (string-append " " text) width))
      (t text))))

(def probe-pad-right
  (lambda (text width)
    (cond
      ((< (string-length text) width)
       (probe-pad-right (string-append text " ") width))
      (t text))))

(def probe-distance-text
  (lambda (distance2)
    (string-append
      (number->string (quotient distance2 2))
      (cond
        ((eq (mod distance2 2) 0) ".0")
        (t ".5")))))

(def probe-marker-order
  (lambda (canon)
    (probe-unique (map pratyahara-row-marker canon))))

(def probe-sound-order
  (lambda (canon)
    (map cadr (sound-ids/42 canon))))

(def probe-entry
  (lambda (canon start marker)
    (let ((members (resolve-pratyahara/last-global canon start marker)))
      (cond
        ((atom members) (quote ()))
        (t (list (string-append start marker) members))))))

(def probe-entries-for-sound-onto
  (lambda (canon start markers acc)
    (cond
      ((atom markers) (reverse acc))
      (t
       (let ((entry (probe-entry canon start (car markers))))
         (cond
           ((atom entry)
            (probe-entries-for-sound-onto
              canon start (cdr markers) acc))
           (t
            (probe-entries-for-sound-onto
              canon start (cdr markers) (cons entry acc)))))))))

(def probe-entries-for-sound
  (lambda (canon start markers)
    (probe-entries-for-sound-onto
      canon start markers (quote ()))))

(def probe-build-pratyaharas
  (lambda (canon)
    (let ((markers (probe-marker-order canon)))
      (reduce
        append
        (quote ())
        (map
          (lambda (sound)
            (probe-entries-for-sound canon sound markers))
          (probe-sound-order canon))))))

(def probe-entry-members
  (lambda (key entries)
    (let ((row (assoc key entries)))
      (cond ((atom row) (quote ())) (t (cadr row))))))

(def probe-keys-containing
  (lambda (sound entries)
    (map
      car
      (filter
        (lambda (entry) (member? sound (cadr entry)))
        entries))))

(def probe-canonical-sounds
  (lambda (canon)
    (map cadr (canonical-positions/43 canon))))

(def probe-nonac
  (lambda (canon ac)
    (filter
      (lambda (sound) (not (member? sound ac)))
      (probe-canonical-sounds canon))))

(def probe-result-row
  (lambda (uk-row entries)
    (let* ((uk (car uk-row))
           (nearest (probe-nearest uk-row))
           (sa (car nearest))
           (distance2 (cadr nearest))
           (inside
             (probe-take
               (probe-sort-strings
                 (probe-keys-containing sa entries))
               6)))
      (list uk sa distance2 inside))))

(def probe-result-rows
  (lambda (entries)
    (map
      (lambda (uk-row) (probe-result-row uk-row entries))
      probe-uk-features)))

(def probe-result-by-uk
  (lambda (uk rows)
    (assoc uk rows)))

(def probe-row-text
  (lambda (row)
    (string-append
      (probe-pad-right (car row) 4)
      (string-append
        (probe-pad-right (cadr row) 10)
        (string-append
          (probe-pad-left (probe-distance-text (third row)) 6)
          (string-append
            "  "
            (probe-join (fourth row) ", ")))))))

(def probe-anchor-text
  (lambda (rows uk expected why)
    (let* ((row (probe-result-by-uk uk rows))
           (got (cadr row))
           (status (cond ((equal? got expected) "OK") (t "FAIL"))))
      (string-append
        "  "
        (string-append
          uk
          (string-append
            " -> "
            (string-append
              got
              (string-append
                " (expected "
                (string-append
                  expected
                  (string-append
                    ") ["
                    (string-append
                      why
                      (string-append "] " status))))))))))))

(def probe-anchors-ok?
  (lambda (rows)
    (and
      (equal? (cadr (probe-result-by-uk "п" rows)) "p")
      (equal? (cadr (probe-result-by-uk "б" rows)) "b")
      (equal? (cadr (probe-result-by-uk "т" rows)) "t")
      (equal? (cadr (probe-result-by-uk "н" rows)) "n"))))

(def probe-report-lines
  (lambda ()
    (let* ((canon (read-siva-sutras-canon))
           (entries (probe-build-pratyaharas canon))
           (ac (probe-entry-members "ac" entries))
           (nonac (probe-nonac canon ac))
           (rows (probe-result-rows entries)))
      (append
        (list
          "=== canonical pratyāhāra coverage ==="
          (string-append
            "  ac   ("
            (string-append
              (probe-pad-left (number->string (length ac)) 2)
              (string-append ") = " (probe-join ac " "))))
          (string-append
            "  non-ac("
            (string-append
              (probe-pad-left (number->string (length nonac)) 2)
              (string-append ") = " (probe-join nonac " "))))
          ""
          "=== Ukrainian phoneme → nearest Sanskrit sound ==="
          "укр  nearest      dist  pratyāhāras containing nearest")
        (append
          (map probe-row-text rows)
          (list
            ""
            "=== sanity anchors (known answers must hold) ==="
            (probe-anchor-text rows "п" "p" "voiceless labial stop → p")
            (probe-anchor-text rows "б" "b" "voiced labial stop → b")
            (probe-anchor-text rows "т" "t" "dental stop → t")
            (probe-anchor-text rows "н" "n" "dental nasal → n")
            ""
            (string-append
              "VERDICT: "
              (cond
                ((probe-anchors-ok? rows)
                 "anchors hold — probe is calibrated")
                (t
                 "ANCHORS FAILED — recalibrate before interpreting anything")))))))))

(def probe-report
  (lambda ()
    (string-append
      (probe-join (probe-report-lines) "\n")
      "\n")))

; CLI-compatible entry point is intentionally separate from the pure report.
(def run-upc8-pratyahara-probe
  (lambda ()
    (princ (probe-report))))
