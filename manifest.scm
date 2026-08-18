;; Guix manifest for shiva-sutras.
;;
;; Usage:
;;   wsl -u siva-sutras
;;   cd /mnt/c/GitHub/shiva-sutras
;;   guix shell -m manifest.scm --
;;
;; WSL user is "siva-sutras" (no h) -- distinct from the swarm-node
;; identity "shiva-sutras-1" (with h), which matches repo.my and the
;; actual repo directory name. Two different namespaces, don't conflate.
;;
;; python-ortools (used by experiments/adversarial/c1p_joint_optimization.py
;; for the CP-SAT decision problem behind M-min=14) is NOT available in
;; Guix (checked via `guix search ortools`, 2026-08-18 -- no match).
;; Install it via pip inside the guix shell instead:
;;   guix shell -m manifest.scm -- python -m pip install --user ortools
;; This manifest does not silently paper over that gap -- `guix shell
;; --pure` will make the missing dependency loud instead of working by
;; accident off an ambient system Python, the same principle cml's own
;; manifest.scm documents for its own accidental-dependency drift finding.

(specifications->manifest
 (list "python"
       "python-pyyaml"
       "python-networkx"
       "git"))
