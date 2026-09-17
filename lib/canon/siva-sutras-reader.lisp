; lib/canon/siva-sutras-reader.lisp
; Native my-lisp reader for the committed Śiva-sūtra canon projections.
;
; ECO-CANON-1 / ECO-LISP-SCRIPTS-1:
;   - ksetra/canon/siva-sutras.yaml remains transmitted/canonical authority;
;   - ksetra/canon/siva-sutras-encoded.yaml is the existing SLP1 engineering
;     projection and explicitly points back to that authority;
;   - this reader contains no second copy of the 14 sutras;
;   - sounds and it-markers remain distinct values;
;   - consumers receive ordinary Lisp data and no longer need Python/YAML.
;
; Supported input is intentionally the narrow committed canon schema, not
; general YAML. This is a structural projection reader, not a YAML library.

(def canon-yaml-path "ksetra/canon/siva-sutras.yaml")
(def canon-slp1-yaml-path "ksetra/canon/siva-sutras-encoded.yaml")

(def split-lines-onto
  (lambda (remaining current acc)
    (cond
      ((string-empty? remaining)
       (reverse (cons current acc)))
      ((eq (string-first remaining) "\n")
       (split-lines-onto (string-rest remaining) "" (cons current acc)))
      (t
       (split-lines-onto
         (string-rest remaining)
         (string-append current (string-first remaining))
         acc)))))

(def split-lines
  (lambda (text) (split-lines-onto text "" (quote ()))))

(def trim-left
  (lambda (text)
    (cond
      ((string-empty? text) text)
      ((eq (string-first text) " ") (trim-left (string-rest text)))
      ((eq (string-first text) "\t") (trim-left (string-rest text)))
      (t text))))

(def after-prefix
  (lambda (prefix text)
    (string-slice text (string-length prefix) (string-length text))))

(def append-token-if-any
  (lambda (token acc)
    (cond
      ((string-empty? token) acc)
      (t (cons token acc)))))

; Parse the restricted YAML inline string list used by both canon files:
;   sounds: ["a", "i", "u"]
; Quotes, brackets and spaces are syntax; comma closes one token.
(def parse-sounds-chars
  (lambda (remaining token acc)
    (cond
      ((string-empty? remaining)
       (reverse (append-token-if-any token acc)))
      (t
       (let ((ch (string-first remaining))
             (rest (string-rest remaining)))
         (cond
           ((eq ch ",")
            (parse-sounds-chars rest "" (append-token-if-any token acc)))
           ((eq ch "]")
            (reverse (append-token-if-any token acc)))
           ((eq ch "[") (parse-sounds-chars rest token acc))
           ((eq ch "\"") (parse-sounds-chars rest token acc))
           ((eq ch " ") (parse-sounds-chars rest token acc))
           ((eq ch "\t") (parse-sounds-chars rest token acc))
           (t (parse-sounds-chars rest (string-append token ch) acc))))))))

(def parse-sounds-line
  (lambda (line)
    (parse-sounds-chars (after-prefix "sounds:" line) "" (quote ()))))

(def parse-marker-chars
  (lambda (remaining acc)
    (cond
      ((string-empty? remaining) acc)
      (t
       (let ((ch (string-first remaining))
             (rest (string-rest remaining)))
         (cond
           ((eq ch "\"") (parse-marker-chars rest acc))
           ((eq ch " ") (parse-marker-chars rest acc))
           ((eq ch "\t") (parse-marker-chars rest acc))
           (t (parse-marker-chars rest (string-append acc ch)))))))))

(def parse-marker-line
  (lambda (marker-prefix line)
    (parse-marker-chars (after-prefix marker-prefix line) "")))

(def canon-row
  (lambda (id sounds marker)
    (list
      id
      (cons (quote sounds) sounds)
      (cons (quote it-marker) marker))))

(def parse-canon-lines-onto
  (lambda (lines marker-prefix next-id pending-sounds acc)
    (cond
      ((atom lines) (reverse acc))
      (t
       (let ((line (trim-left (car lines))))
         (cond
           ((string-prefix? "sounds:" line)
            (parse-canon-lines-onto
              (cdr lines)
              marker-prefix
              next-id
              (parse-sounds-line line)
              acc))
           ((string-prefix? marker-prefix line)
            (cond
              ((atom pending-sounds)
               (canon-reader-marker-without-sounds next-id line))
              (t
               (parse-canon-lines-onto
                 (cdr lines)
                 marker-prefix
                 (+ next-id 1)
                 (quote ())
                 (cons
                   (canon-row
                     next-id
                     pending-sounds
                     (parse-marker-line marker-prefix line))
                   acc)))))
           (t
            (parse-canon-lines-onto
              (cdr lines) marker-prefix next-id pending-sounds acc))))))))

(def parse-siva-sutras-yaml
  (lambda (text marker-prefix)
    (parse-canon-lines-onto
      (split-lines text) marker-prefix 1 (quote ()) (quote ()))))

(def read-siva-sutras-canon
  (lambda ()
    (parse-siva-sutras-yaml
      (read-file canon-yaml-path)
      "it_marker_iast:")))

(def read-siva-sutras-slp1
  (lambda ()
    (parse-siva-sutras-yaml
      (read-file canon-slp1-yaml-path)
      "it_marker_slp1:")))
