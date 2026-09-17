; test_pratyahara_masks.lisp — native my-lisp regression for pratyāhāra masks
; Replaces the new Python-only regression direction with an executable Lisp
; check over the canonical .lisp knowledge-base surface.
;
; Run from the shiva-sutras repository with a my-lisp-cli binary:
;   my-lisp-cli prototype/lisp_core_phonetics/test_pratyahara_masks.lisp
;
; Or from a sibling my-lisp checkout:
;   cargo run -p my-lisp-cli -- ../shiva-sutras/prototype/lisp_core_phonetics/test_pratyahara_masks.lisp

(def phonetics-kb
  (read (read-file "prototype/lisp_core_phonetics/prototype_phonetics.lisp")))

(def pratyahara-masks
  (cdr (assoc (quote pratyahara-masks) phonetics-kb)))

(def mask-of
  (lambda (name)
    (cdr
      (assoc
        (quote mask)
        (cdr (assoc name pratyahara-masks))))))

(def require-mask
  (lambda (name expected)
    (cond
      ((eq (mask-of name) expected) (quote ok))
      (t (pratyahara-mask-regression-failed name (mask-of name) expected)))))

; Corrected reference values backported from juv4uk/my-lisp.
; These are derived engineering masks, not a replacement for the immutable
; Śiva-sūtra canon in ksetra/canon/siva-sutras.yaml.
(require-mask (quote ac)  #x00000000000001FF)
(require-mask (quote hal) #x000007FFFFFFFE00)
(require-mask (quote al)  #x000007FFFFFFFFFF)
(require-mask (quote ik)  #x000000000000001E)
(require-mask (quote ec)  #x00000000000001E0)
(require-mask (quote yar) #x000003FFFFFFFC00)
(require-mask (quote Sar) #x000003800000000000)
(require-mask (quote JaS) #x000000001F00000000)
(require-mask (quote Jal) #x000003FFFF000200)

(print (quote pratyahara-mask-regression-green))
