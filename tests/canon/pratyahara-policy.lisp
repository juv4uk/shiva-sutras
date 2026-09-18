; tests/canon/pratyahara-policy.lisp
; Repeated-marker policy witness for issue #17.

(load "lib/canon/pratyahara.lisp")

(def require-equal
  (lambda (label actual expected)
    (cond
      ((equal? actual expected) (quote ok))
      (t (pratyahara-policy-regression label actual expected)))))

(def iast-canon (read-siva-sutras-canon))
(def slp1-canon (read-siva-sutras-slp1))

(require-equal
  (quote iast-first-a-n)
  (resolve-pratyahara/first-after-start iast-canon "a" "ṇ")
  (quote ("a" "i" "u")))

(require-equal
  (quote iast-last-a-n)
  (resolve-pratyahara/last-global iast-canon "a" "ṇ")
  (quote ("a" "i" "u" "ṛ" "ḷ" "e" "o" "ai" "au" "h" "y" "v" "r" "l")))

(require-equal
  (quote slp1-first-a-R)
  (resolve-pratyahara/first-after-start slp1-canon "a" "R")
  (quote ("a" "i" "u")))

(require-equal
  (quote slp1-last-a-R)
  (resolve-pratyahara/last-global slp1-canon "a" "R")
  (quote ("a" "i" "u" "f" "x" "e" "o" "E" "O" "h" "y" "v" "r" "l")))

; Non-repeated marker: policies must converge.
(require-equal
  (quote iast-ac-policy-convergence)
  (resolve-pratyahara/first-after-start iast-canon "a" "c")
  (resolve-pratyahara/last-global iast-canon "a" "c"))

(print (quote pratyahara-marker-policy-green))
