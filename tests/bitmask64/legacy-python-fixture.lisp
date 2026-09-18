; tests/bitmask64/legacy-python-fixture.lisp
; Historical migration evidence captured from the final GREEN Python oracle
; before prototype/bitmask64/bitmask64.py was retired.
;
; NON-AUTHORITATIVE: these values preserve what the legacy implementation did;
; they do not define current pratyahara semantics.

(def bitmask64-legacy-python-fixture
  (quote
    ((python-tests . 7)
     (python-tests-status . green)
     (canonical-sound-count . 42)
     (named-table-unique-keys . 41)
     (c-header
       (bytes . 3133)
       (sha256 . "f419374e60c86b9fa7fe3aa84d94a5ad1182063bf3fd04c70f92ef21eb3f6f78"))
     (verilog
       (bytes . 302)
       (sha256 . "ed8a9f26363d38c2049ced46606ff8f03f63786ff1ae66a78ca934822f948a05"))
     (disputed-masks
       (val . #x000003FFFFFFFC00)
       (ral . #x000003FFFFFFF000)
       (iR  . #x0000000000003FFE)
       (eR  . #x0000000000000060)
       (nam . #x0000000000070000)
       (xay . #x0000001FE0000000)
       (caw . #x0000000C00000000)))))
