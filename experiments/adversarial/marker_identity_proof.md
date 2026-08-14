# Experiment 5.7: It-Marker Identity Constraints

Testing if the two valid geometrical classes can support the historical, unambiguous naming of pratyāhāras (especially `eṅ`, `aic`, `ec`, `ac`).

## 1. Class B (Canonical) Analysis
In Class B, Block 2 is `{e, o}` and Block 3 is `{ai, au}`.
- The set for historical `eṅ` is `{e, o}`. It spans Block 2. It starts at `e` and requires a marker after Block 2. We can assign $M_2 = ṅ$. Name: **eṅ**.
- The set for historical `aic` is `{ai, au}`. It spans Block 3. It starts at `ai` and requires a marker after Block 3. We can assign $M_3 = c$. Name: **aic**.
- The set for historical `ec` is `{e, o, ai, au}`. It spans Blocks 2 and 3. It starts at `e` (in Block 2) and requires a marker after Block 3. Marker after Block 3 is already $c$. Name: **ec**.
- The set for historical `ac` (all vowels). It spans Blocks 0 to 3. It starts at `a` and ends after Block 3. Marker is $c$. Name: **ac**.
**Result for Class B:** PERFECT. No naming collisions. The identities $M_2 = ṅ$ and $M_3 = c$ produce unambiguous, historically accurate addresses.

## 2. Class A (Swapped) Analysis
In Class A, Block 2 is `{ai, au}` and Block 3 is `{e, o}`.
- The set for `{ai, au}` spans Block 2. It starts at `ai`. Needs a marker after Block 2 ($M_2$). Let's call the name `ai` + $M_2$.
- The set for `{e, o}` spans Block 3. It starts at `e`. Needs a marker after Block 3 ($M_3$). Let's call the name `e` + $M_3$.
- The set for ALL FOUR `{ai, au, e, o}` spans Blocks 2 and 3. Because `ai` is first, it MUST start with `ai`. It ends after Block 3, so its marker is $M_3$. Name: **`ai` + $M_3$**.

Now consider the constraint from the full vowel set `ac`:
- `ac` must cover Blocks 0 to 3. It starts at `a` and ends after Block 3. To historically be named `ac`, the marker $M_3$ MUST be $c$.
- If $M_3 = c$, then the pratyāhāra for `{e, o}` becomes **ec**.
- If $M_3 = c$, then the pratyāhāra for `{ai, au, e, o}` becomes **aic**.
- But what about `{ai, au}` (Block 2)? If we set $M_2 = c$, its name is **aic**. But then `{ai, au}` and `{ai, au, e, o}` would BOTH be named **aic**! A fatal collision.
- If we set $M_2 = ṅ$, its name is **aiṅ**. Then `{ai, au}` is **aiṅ**, `{e, o}` is **ec**, and `{ai, au, e, o}` is **aic**.

**FATAL FLAW FOR CLASS A:**
Even though we can avoid a mathematical collision by setting $M_2=ṅ$ and $M_3=c$, doing so fundamentally breaks the historical naming map:
1. `{e, o, ai, au}` would be named **aic** instead of historical **ec**.
2. `{ai, au}` would be named **aiṅ** instead of historical **aic**.
3. `{e, o}` would be named **ec** instead of historical **eṅ**.

**Conclusion:** Class A is fundamentally incapable of supporting Pāṇini's exact historical marker addresses and phonological grouping semantics. Only Class B (Canonical) can support both the M=14 optimal geometry AND the exact historical addresses!
