# UPC-7 prototype: 7-bit identities, switchable human layouts

**Status:** experimental engineering prototype for #27.

UPC-7 is derived from the existing UPC-8 prototype without renumbering its
currently assigned lower-plane codes.

## Identity law

```text
UPC-7 identity = exactly 7 bits
0000000 .. 1111111
0x00    .. 0x7F
```

Current UPC-8 assigned entries are already entirely below `0x80`, so the
first UPC-7 prototype uses an identity-preserving projection:

```text
UPC7(code) = UPC8(code), code <= 0x7F
```

No modulo, truncation, aliasing, or high-bit stripping is allowed.

## Layout law

A layout is a human input/output mapping over a code identity. It does not own
the identity.

```text
host spelling --encode(layout)--> UPC-7 codes --render(layout)--> host spelling
```

Changing a layout must leave the middle sequence unchanged.

Initial layouts:

- `sa-slp1`: Sanskrit engineering SLP1 spellings inherited from UPC-8;
- `uk`: Ukrainian mappings inherited from UPC-8;
- `bits`: exact 7-bit diagnostic cells, e.g. `0100101 0000001`.

The human layouts are intentionally partial. If a code has no justified
spelling in the requested layout, rendering fails. This prevents a
near-equivalent phoneme from silently becoming an identity alias.

Example:

```text
sa-slp1: kim
              \
               -> same UPC-7 code stream -> uk: кім
```

This works because `k`/к, `i`/і and `m`/м already share explicit UPC-8
identities.

By contrast Sanskrit `a` and Ukrainian `а` currently have different codes
(`0x00` vs `0x33`, the latter classified as near-equivalent), so switching
that code to the Ukrainian layout fails closed instead of silently merging
them.

## Relation to SENS

Candidate target:

```text
SENS
  structure : ( )
  Function  : 8-bit
  Number    : binary
  Text      : sequence of UPC-7 identities
```

Python/Unicode strings in this prototype are only host UI transport. They are
not UPC-7 identities and are not proposed as SENS Text.

## Storage width

UPC-7 is logically seven bits. This first Python prototype returns integer
tuples (and the donor UPC-8 uses bytes), so host memory may temporarily spend
8+ bits per cell. Bit-packing is a separate transport/storage problem and must
not be confused with the semantic code width.

A future packed form can store 8 UPC-7 cells in 7 bytes without changing code
identity, but it needs its own round-trip and boundary tests.

## Non-claim

This is an engineering codec/projection. It is not evidence that Pāṇini used
binary codes, and it does not modify the transmitted Śiva-sūtra canon.
