; tests/upc8/pratyahara-probe.lisp
; Differential migration witness for prototype/upc8_pratyahara_probe/probe.py.

(load "prototype/upc8_pratyahara_probe/probe.lisp")

(def require-equal
  (lambda (label actual expected)
    (cond
      ((equal? actual expected) (quote ok))
      (t (upc8-pratyahara-probe-regression label actual expected)))))

(def probe-canon (read-siva-sutras-canon))
(def probe-entries (probe-build-pratyaharas probe-canon))
(def probe-rows (probe-result-rows probe-entries))

(require-equal (quote probe-entry-count) (length probe-entries) 301)
(require-equal
  (quote legacy-a-n-last-global)
  (probe-entry-members "aṇ" probe-entries)
  (quote ("a" "i" "u" "ṛ" "ḷ" "e" "o" "ai" "au" "h" "y" "v" "r" "l")))

(require-equal (quote nearest-p) (cadr (probe-result-by-uk "п" probe-rows)) "p")
(require-equal (quote nearest-b) (cadr (probe-result-by-uk "б" probe-rows)) "b")
(require-equal (quote nearest-t) (cadr (probe-result-by-uk "т" probe-rows)) "t")
(require-equal (quote nearest-n) (cadr (probe-result-by-uk "н" probe-rows)) "n")
(require-equal (quote nearest-zh) (cadr (probe-result-by-uk "ж" probe-rows)) "ś")
(require-equal (quote nearest-zh-distance2) (third (probe-result-by-uk "ж" probe-rows)) 6)

(def report (probe-report))
(write-file "/workspace/notes/upc8-pratyahara-probe-lisp.txt" report)
(print (list (quote probe-report-sha256) (sha256-hex report)))
(print (quote upc8-pratyahara-probe-semantic-green))
