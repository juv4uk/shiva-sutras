# 64-Bit Pratyāhāra Bitmask Engine

**Status:** Layer 6 Engineering Prototype · Lisp migration in progress (#19)  
**Sound universe:** 42 unique Canon-derived IDs  
**Named legacy table:** 41 unique Python keys (the old 42-key / 336-byte claim is not currently an authority)  
**Current Lisp correctness backend:** exact arithmetic over 42 positions, O(42) worst-case per set operation  
**Planned machine backend:** integer bitwise mechanism tracked in `my-lisp#585`; only that backend may justify native-word / one-instruction performance claims

## Overview
The 42 unique canonical sounds of the Śiva Sūtras fit within the lower 42 bits of a single standard 64-bit machine word (`uint64_t`). This enables instant parallel set operations using native CPU ALU instructions or single-cycle FPGA lookups.

## Named-table status

The historical Python source contains 42 literal rows but defines `hal` twice, so the live dictionary has **41 unique keys**. Several legacy names are also under separate semantic review (`val`, `ral`, `iR`, `eR`, `nam`, `xay`, `caw`). Therefore this README no longer treats a 42-row/336-byte named ROM as established fact.

The safe invariant is narrower: the Canon-derived **sound identity universe has 42 bits** and fits in a 64-bit word. Named pratyāhāra masks must be generated from an explicit resolver policy rather than copied from the old table.

## Hardware Implementation (Verilog)
