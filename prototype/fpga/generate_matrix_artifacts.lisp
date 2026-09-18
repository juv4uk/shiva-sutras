; prototype/fpga/generate_matrix_artifacts.lisp
; Compatibility entry point replacing gen_matrix.py.
; Preserves the historical output destination used by the prototype.

(load "prototype/fpga/gen_matrix.lisp")

(def generated-matrix (build-pratyahara-matrix))
(write-pratyahara-artifacts generated-matrix "/workspace/notes")

(print
  (list
    (quote fpga-matrix-artifacts-written)
    (matrix-sound-count)
    (length generated-matrix)))
