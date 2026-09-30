; UPC-7 cold witness (shiva-sutras#33).
;
; An independent reader of the generated machine table `upc7-table.tsv`.
; It shares NO code with the Python producer (`upc7_geometry.py`,
; `upc7_layouts.py`, `upc7_table.py`): it re-derives every cell's bits, hex,
; class and payload from the row position alone, and checks the table against
; the geometry laws stated in UPC7-GEOMETRY-v2.md, not against Python output.
;
; Usage (from the repository root):   sens prototype/upc7_cold_witness.lisp
; Exit is non-zero on the first failing witness set.
;
; Agreement between two independent substrates is stronger evidence than more
; tests inside one implementation.

; ---- pinned provenance -------------------------------------------------
; A consumer pins this SHA-256 of the table it trusts. Changing the table
; without changing this pin fails the witness on purpose.
(00001001 w-pinned-sha256
  "dbceb2733247801e2434aad27427138bacd35b7755faa0223f3cbf91240ccca6")

(00001001 w-table-path "prototype/upc7-table.tsv")

; ---- small w-text and list helpers ---------------------------------------
(00001001 w-s+ (00001000 (a b) (00111010 a b)))
; Null test via equal?: yields exactly 1/0 on every runtime (ATOM on () does not yet).
(00001001 w-yes (00100010 0 0))
(00001001 w-no (00100010 0 1))
(00001001 w-nul? (00001000 (l) (00100010 l ())))
(00001001 w-same? (00001000 (a b) (00100010 a b)))
(00001001 w-list2 (00001000 (a b) (00000100 a (00000100 b ()))))
(00001001 w-second (00001000 (l) (00000101 (00000110 l))))
(00001001 w-nth3 (00001000 (l) (00000101 (00000110 (00000110 l)))))
(00001001 w-nth4 (00001000 (l) (00000101 (00000110 (00000110 (00000110 l))))))
(00001001 w-nth5 (00001000 (l) (00000101 (00000110 (00000110 (00000110 (00000110 l)))))))
(00001001 w-nth6 (00001000 (l) (00000101 (00000110 (00000110 (00000110 (00000110 (00000110 l))))))))
(00001001 w-nth7 (00001000 (l) (00000101 (00000110 (00000110 (00000110 (00000110 (00000110 (00000110 l)))))))))
(00001001 w-nth8 (00001000 (l) (00000101 (00000110 (00000110 (00000110 (00000110 (00000110 (00000110 (00000110 l))))))))))

(00001001 w-append
  (00001000 (a b)
    (00000111
      ((w-nul? a) b)
      (w-yes (00000100 (00000101 a) (w-append (00000110 a) b))))))

(00001001 w-map-prefix
  (00001000 (prefix l)
    (00000111
      ((w-nul? l) ())
      (w-yes (00000100 (w-s+ prefix (00000101 l)) (w-map-prefix prefix (00000110 l)))))))

; Text starts with marker (as a predicate bit).
(00001001 w-starts? (00001000 (marker s) (00000011 t (00111101 marker s))))
(00001001 w-has? (00001000 (needle s) (00000011 t (00111110 needle s))))

; Split `s` at the first `sep` character: (before after).
(00001001 w-take-until
  (00001000 (s sep acc)
    (00000111
      ((00100010 (00111011 s) 0) (w-list2 acc ""))
      ((00100010 (00111111 s) sep) (w-list2 acc (01000000 s)))
      (w-yes (w-take-until (01000000 s) sep (w-s+ acc (00111111 s)))))))

(00001001 w-split
  (00001000 (s sep)
    (00000111
      ((00100010 (00111011 s) 0) ())
      (w-yes (00000100 (00000101 (w-take-until s sep ""))
                   (w-split (w-second (w-take-until s sep "")) sep))))))

(00001001 w-join
  (00001000 (l sep)
    (00000111
      ((w-nul? l) "")
      ((w-nul? (00000110 l)) (00000101 l))
      (w-yes (w-s+ (00000101 l) (w-s+ sep (w-join (00000110 l) sep)))))))

; Force a row to exactly 8 fields; extra fields are reported separately.
(00001001 w-pad-to
  (00001000 (template l)
    (00000111
      ((w-nul? template) ())
      ((w-nul? l) (00000100 "" (w-pad-to (00000110 template) ())))
      (w-yes (00000100 (00000101 l) (w-pad-to (00000110 template) (00000110 l)))))))
(00001001 w-longer?
  (00001000 (l template)
    (00000111
      ((w-nul? l) w-no)
      ((w-nul? template) w-yes)
      (w-yes (w-longer? (00000110 l) (00000110 template))))))

(00001001 w-member?
  (00001000 (x l)
    (00000111
      ((w-nul? l) w-no)
      ((w-same? x (00000101 l)) w-yes)
      (w-yes (w-member? x (00000110 l))))))

; Non-empty entries that occur more than once.
(00001001 w-duplicates
  (00001000 (l)
    (00000111
      ((w-nul? l) ())
      ((00100010 (00000101 l) "") (w-duplicates (00000110 l)))
      ((w-member? (00000101 l) (00000110 l))
       (00000100 (00000101 l) (w-duplicates (00000110 l))))
      (w-yes (w-duplicates (00000110 l))))))

(00001001 w-assoc
  (00001000 (key pairs)
    (00000111
      ((w-nul? pairs) "?")
      ((w-same? key (00000101 (00000101 pairs))) (w-second (00000101 pairs)))
      (w-yes (w-assoc key (00000110 pairs))))))

; 5-bit and 7-bit binary strings compare like numbers, character by character.
(00001001 w-bits-less?
  (00001000 (a b)
    (00000111
      ((00100010 (00111011 a) 0) w-no)
      ((w-same? (00111111 a) (00111111 b)) (w-bits-less? (01000000 a) (01000000 b)))
      (w-yes (w-same? (00111111 a) "0")))))

; ---- independent geometry, derived from position only -------------------
; All 128 seven-bit strings in ascending order, built without arithmetic.
(00001001 w-all-bits
  (00001000 (template)
    (00000111
      ((w-nul? template) (00000100 "" ()))
      (w-yes (w-append (w-map-prefix "0" (w-all-bits (00000110 template)))
                 (w-map-prefix "1" (w-all-bits (00000110 template))))))))
(00001001 w-seven-slots (00001000 () (00000100 1 (00000100 1 (00000100 1 (00000100 1 (00000100 1 (00000100 1 (00000100 1 ())))))))))

(00001001 w-nibbles
  (00001000 ()
    (00000100 (w-list2 "0000" "0") (00000100 (w-list2 "0001" "1") (00000100 (w-list2 "0010" "2") (00000100 (w-list2 "0011" "3")
    (00000100 (w-list2 "0100" "4") (00000100 (w-list2 "0101" "5") (00000100 (w-list2 "0110" "6") (00000100 (w-list2 "0111" "7")
    (00000100 (w-list2 "1000" "8") (00000100 (w-list2 "1001" "9") (00000100 (w-list2 "1010" "A") (00000100 (w-list2 "1011" "B")
    (00000100 (w-list2 "1100" "C") (00000100 (w-list2 "1101" "D") (00000100 (w-list2 "1110" "E") (00000100 (w-list2 "1111" "F") ()))))))))))))))))))

(00001001 w-class-names
  (00001000 ()
    (00000100 (w-list2 "00" "varga") (00000100 (w-list2 "01" "non-varga")
    (00000100 (w-list2 "10" "vowel") (00000100 (w-list2 "11" "sign/operator") ()))))))

(00001001 w-class-prefixes
  (00001000 ()
    (00000100 (w-list2 "varga" "varga.") (00000100 (w-list2 "non-varga" "non-varga.")
    (00000100 (w-list2 "vowel" "vowel.") (00000100 (w-list2 "sign/operator" "sign.") ()))))))

(00001001 w-expected-hex
  (00001000 (e)
    (w-s+ "0x" (w-s+ (w-assoc (w-s+ "0" (01000001 e 0 3)) (w-nibbles)) (w-assoc (01000001 e 3 7) (w-nibbles))))))

; ---- witnesses over one row ---------------------------------------------
(00001001 w-need
  (00001000 (ok message)
    (00000111
      (ok ())
      (w-yes (00000100 message ())))))

(00001001 w-nth1 (00001000 (l) (00000101 l)))
(00001001 w-nth2 w-second)

;---- header-driven columns ---------------------------------------------
; The first six columns (bits hex class payload status name) are the contract of the table.
; Every spelling column (sa-slp1, sa-iast, sa-deva, uk, ...) is found BY NAME in the header,
; so a new layout column cannot silently shift another one (it did once: #42).
(00001001 w-field
  (00001000 (header row name)
    (00000111
      ((w-nul? header) "")
      ((w-same? (00000101 header) name) (00000101 row))
      (w-yes (w-field (00000110 header) (00000110 row) name)))))

(00001001 w-blanks
  (00001000 (header)
    (00000111
      ((w-nul? header) ())
      (w-yes (00000100 "" (w-blanks (00000110 header)))))))

; All spellings of a row, joined: a reserved cell must have none in ANY layout.
(00001001 w-spellings
  (00001000 (header row)
    (w-s+ (w-field header row "sa-slp1")
      (w-s+ (w-field header row "sa-iast")
        (w-s+ (w-field header row "sa-deva") (w-field header row "uk"))))))

; One row, already w-split into its fields, against its position `e`.
(00001001 w-row-failures8
  (00001000 (bits hex klass payload status name sa uk e)
    (w-append
      (w-need (w-same? bits e) (w-s+ "bits differ from row position: " (w-s+ bits (w-s+ " vs " e))))
      (w-append
        (w-need (w-same? hex (w-expected-hex e)) (w-s+ "hex disagrees with bits: " bits))
        (w-append
          (w-need (w-same? klass (w-assoc (01000001 e 0 2) (w-class-names))) (w-s+ "class disagrees with top bits: " bits))
          (w-append
            (w-need (w-same? payload (01000001 e 2 7)) (w-s+ "payload disagrees with low bits: " bits))
            (w-append
              (w-need (w-member? status (00000100 "assigned" (00000100 "reserved" ())))
                    (w-s+ "status is neither assigned nor reserved: " bits))
              (w-append
                (w-status-failures bits klass payload status name sa uk)
                (w-append
                  (w-varga-failures bits klass payload status)
                  (w-vowel-failures bits klass payload status name))))))))))

(00001001 w-status-failures
  (00001000 (bits klass payload status name sa uk)
    (00000111
      ((w-same? status "reserved")
       (w-append
         (w-need (w-same? name (w-s+ "reserved." (w-s+ klass (w-s+ "." payload)))) (w-s+ "reserved cell has a wrong name: " bits))
         (w-need (w-same? (w-s+ sa uk) "") (w-s+ "reserved cell has a spelling: " bits))))
      (w-yes (w-need (w-starts? (w-assoc klass (w-class-prefixes)) name) (w-s+ "assigned name does not match class: " bits))))))

; Varga law: 25 cells (5 places x 5 members) are assigned, the rest reserved.
(00001001 w-varga-failures
  (00001000 (bits klass payload status)
    (00000111
      ((w-same? klass "varga")
       (w-need (w-same? (w-same? status "assigned") (w-bits-less? payload "11001"))
             (w-s+ "varga assignment breaks the 5x5 law: " bits)))
      (w-yes ()))))

; Vowel law: rows 0..6 carry nasal/length in the low two payload bits; row 7
; is the extension row and does not.
(00001001 w-vowel-failures
  (00001000 (bits klass payload status name)
    (00000111
      ((w-same? klass "vowel")
       (00000111
         ((w-same? status "assigned")
          (00000111
            ((w-same? (01000001 payload 0 3) "111")
             (w-need (w-starts? "vowel.uk-ext." name) (w-s+ "row 7 cell is not an extension cell: " bits)))
            (w-yes (w-append
                 (w-need (w-same? (w-has? ".nasal." name) (w-same? (01000001 payload 3 4) "1"))
                       (w-s+ "nasal bit disagrees with the name: " bits))
                 (w-need (w-same? (w-has? ".long" name) (w-same? (01000001 payload 4 5) "1"))
                       (w-s+ "length bit disagrees with the name: " bits))))))
         (w-yes ())))
      (w-yes ()))))

(00001001 w-row-failures
  (00001000 (header f e)
    (00000111
      ((w-longer? f (w-blanks header)) (00000100 (w-s+ "more fields than the header: " e) ()))
      (w-yes (w-row-failures8 (w-nth1 f) (w-nth2 f) (w-nth3 f) (w-nth4 f) (w-nth5 f) (w-nth6 f)
                              (w-spellings header f) "" e)))))

; Apply w-row-failures to every (row, expected-bits) pair.
(00001001 w-rows-failures
  (00001000 (header rows expected)
    (00000111
      ((w-nul? rows) ())
      ((w-nul? expected) (00000100 "more rows than 128 cells" ()))
      (w-yes (w-append (w-row-failures header (00000101 rows) (00000101 expected))
                 (w-rows-failures header (00000110 rows) (00000110 expected)))))))

(00001001 w-assigned-only
  (00001000 (rows pick)
    (00000111
      ((w-nul? rows) ())
      ((w-same? (w-nth5 (00000101 rows)) "assigned")
       (00000100 (pick (00000101 rows)) (w-assigned-only (00000110 rows) pick)))
      (w-yes (w-assigned-only (00000110 rows) pick)))))

(00001001 w-same-length?
  (00001000 (a b)
    (00000111
      ((w-nul? a) (w-nul? b))
      ((w-nul? b) w-no)
      (w-yes (w-same-length? (00000110 a) (00000110 b))))))

; Data rows: every line after the header, each padded to the header's length.
(00001001 w-pad-all
  (00001000 (header lines)
    (00000111
      ((w-nul? lines) ())
      (w-yes (00000100 (w-pad-to (w-blanks header) (w-split (00000101 lines) "\t")) (w-pad-all header (00000110 lines)))))))

(00001001 w-header (00001000 (w-text) (w-split (00000101 (w-split w-text "\n")) "\t")))
(00001001 w-data-rows (00001000 (w-text) (w-pad-all (w-header w-text) (00000110 (w-split w-text "\n")))))

; All failures of one table w-text against a pin. `()` means every witness holds.
(00001001 w-table-failures
  (00001000 (w-text pin)
    (w-table-failures-of w-text pin (w-data-rows w-text))))

(00001001 w-column-of
  (00001000 (header name)
    (00001000 (row) (w-field header row name))))

(00001001 w-table-failures-of
  (00001000 (w-text pin rows)
    (w-table-failures-with (w-header w-text) w-text pin rows)))

(00001001 w-table-failures-with
  (00001000 (header w-text pin rows)
    (w-append
      (w-need (w-same? (10100001 w-text) pin) "SHA-256 of the table differs from the pinned SHA-256")
      (w-append
        (w-need (w-same-length? rows (w-all-bits (w-seven-slots))) "the table does not have exactly 128 cells")
        (w-append
          (w-rows-failures header rows (w-all-bits (w-seven-slots)))
          (w-append
            (w-need (w-nul? (w-duplicates (w-assigned-only rows w-nth6))) "two assigned cells share a stable name")
            (w-append
              (w-need (w-nul? (w-duplicates (w-assigned-only rows (w-column-of header "sa-slp1")))) "sa-slp1 spelling names two cells")
              (w-append
                (w-need (w-nul? (w-duplicates (w-assigned-only rows (w-column-of header "sa-iast")))) "sa-iast spelling names two cells")
                (w-append
                  (w-need (w-nul? (w-duplicates (w-assigned-only rows (w-column-of header "sa-deva")))) "sa-deva spelling names two cells")
                  (w-need (w-nul? (w-duplicates (w-assigned-only rows (w-column-of header "uk")))) "uk spelling names two cells"))))))))))

; ---- deliberate mutations: the witness must reject each one -------------
(00001001 w-drop-last
  (00001000 (l)
    (00000111
      ((w-nul? (00000110 l)) ())
      (w-yes (00000100 (00000101 l) (w-drop-last (00000110 l)))))))

; Replace field k of the first data row, keeping everything else byte-identical.
(00001001 w-set-field
  (00001000 (fields k value)
    (00000111
      ((w-nul? fields) ())
      ((00100010 k 1) (00000100 value (00000110 fields)))
      (w-yes (00000100 (00000101 fields) (w-set-field (00000110 fields) (00001100 k -1) value))))))

(00001001 w-mutate-first-row
  (00001000 (w-text k value)
    (w-join (00000100 (00000101 (w-split w-text "\n"))
                    (00000100 (w-join (w-set-field (w-split (w-second (w-split w-text "\n")) "\t") k value) "\t")
                              (00000110 (00000110 (w-split w-text "\n")))))
          "\n")))

(00001001 w-mutate-drop-last-row (00001000 (w-text) (w-join (w-drop-last (w-split w-text "\n")) "\n")))

; ---- run -----------------------------------------------------------------
(00001001 w-print-all
  (00001000 (label failures)
    (00000111
      ((w-nul? failures) 1)
      (w-yes (00000100 (01001000 (w-s+ label (00000101 failures))) ())))))

(00001001 w-text (10100110 w-table-path))

(00001001 w-real-failures (w-table-failures w-text w-pinned-sha256))

; A mutated table must NOT pass: 1 = the witness caught it.
(00001001 w-caught?
  (00001000 (mutated)
    (00000111
      ((w-nul? (w-table-failures mutated w-pinned-sha256)) w-no)
      (w-yes w-yes))))

; Same mutation, but with the SHA pin removed: proves the structural
; witnesses catch it by themselves, not only the hash.
(00001001 w-caught-structurally?
  (00001000 (mutated)
    (00000111
      ((w-nul? (w-table-failures mutated (10100001 mutated))) w-no)
      (w-yes w-yes))))

(00001001 w-fail-run
  (00001000 (message)
    (00101111 (00100111 (01001000 (w-s+ "FAIL: " message)) (00000101 (00000001 ()))))))

(00000111
  ((w-nul? w-real-failures) (01001000 "ok: the table passes every cold witness"))
  (w-yes (w-fail-run (00000101 w-real-failures))))

(00000111
  ((w-caught? (w-mutate-drop-last-row w-text)) (01001000 "ok: dropping a row is rejected"))
  (w-yes (w-fail-run "dropping a row was NOT rejected")))
(00000111
  ((w-caught-structurally? (w-mutate-drop-last-row w-text)) (01001000 "ok: dropping a row is rejected without the SHA"))
  (w-yes (w-fail-run "dropping a row was NOT caught structurally")))
(00000111
  ((w-caught-structurally? (w-mutate-first-row w-text 5 "reserved")) (01001000 "ok: flipping a status is rejected without the SHA"))
  (w-yes (w-fail-run "flipping a status was NOT caught structurally")))
(00000111
  ((w-caught-structurally? (w-mutate-first-row w-text 1 "1111111")) (01001000 "ok: a wrong bits field is rejected without the SHA"))
  (w-yes (w-fail-run "a wrong bits field was NOT caught structurally")))
(00000111
  ((w-caught-structurally? (w-mutate-first-row w-text 2 "0x01")) (01001000 "ok: a wrong hex field is rejected without the SHA"))
  (w-yes (w-fail-run "a wrong hex field was NOT caught structurally")))
(00000111
  ((w-caught-structurally? (w-mutate-first-row w-text 6 "sign.k")) (01001000 "ok: a name that contradicts the class is rejected without the SHA"))
  (w-yes (w-fail-run "a class/name contradiction was NOT caught structurally")))
(00000111
  ((w-caught? (w-mutate-first-row w-text 7 "k")) (01001000 "ok: a one-field change is rejected by the SHA pin"))
  (w-yes (w-fail-run "a one-field change was NOT rejected")))
(01001000 "upc7-cold-witness: all witnesses hold")
