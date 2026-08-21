# Slavic & Ukrainian Phonetics Prototype

**Status:** Layer 6 Engineering Prototype  
**Scope:** UPC-8 extension codes `0x31..0x4F` + Shared codes `0x00..0x29`

## Features
1. **Articulatory Feature Matrix:** Maps Place (Labial, Dental, Postalveolar, Palatal, Velar, Glottal), Manner (Stop, Affricate, Fricative, Nasal, Liquid, Vowel), Voicing, and Palatalization.
2. **Context-Aware Iotated Decomposition:** Accurately decomposes `я, ю, є, ї` based on syllable position and preceding consonant softening.
3. **Geometric Palatalization Shifts:** Formalizes historical Slavic palatalizations ($k \to \check{c}, g \to \check{z}, x \to \check{s}$ and $k \to c', g \to z', x \to s'$) as vector displacements in articulatory feature space.
