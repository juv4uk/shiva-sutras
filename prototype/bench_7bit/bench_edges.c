/* Design-level cost of the sound-graph edges asp / voice / nasal / shift / long computed three ways on the same pairs (research; I refs via Cachegrind).
 *
 *   A  guarded XOR on the 14-bit code:  r = guard(c) ? c ^ mask(c) : c   (no table)
 *   B  the hand table's mixed radix on the 7-bit cell: payload = place*5 + member (varga), place*4 + slot (non-varga), row*4 + nose*2 + long (vowel)
 *   C  a lookup in a table of 128 cells filled in setup from the graph's answer (the knowledge is COPIED, parity by construction)
 *
 * A reads 14-bit codes, B and C 7-bit cells: the cost of getting the code/cell is not measured (the caller holds it).
 * Usage: bench_edges <A|B|C> <asp|voice|nasal|shift|long|null> <calls> <setup|full|check>
 * The method and the edge are chosen ONCE, outside the loop (no per-call string compare).
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "edges.h"

#define UNDEF 0xFFFF

static uint8_t tab[5][128];                       /* method C: edge -> cell -> cell (0xFF = undefined) */

static inline int a_asp(int c)   { return ((c >> 4) & 7) == 0 ? c ^ 0x0001 : UNDEF; }
static inline int a_voice(int c) { return c ^ 0x0002; }
static inline int a_nasal(int c) { return c ^ (((~c) & 0x0082) | (c & 0x0001)); }
static inline int a_shift(int c) { return (c & 0x1000) ? UNDEF : (c & ~0x1F00) | ((c & 0x1F00) << 1); }
static inline int a_long(int c)  { int len = (c >> 2) & 3; return (((c >> 4) & 7) < 3 || len == 2) ? UNDEF : c ^ (len == 0 ? 0x4 : 0xC); }

static inline int b_asp(int h)
{
    int cls = h >> 5, p = h & 31;
    if (cls != 0) return UNDEF;
    int place = p / 5, m = p % 5;
    return m < 4 ? (place * 5 + (m ^ 1)) : UNDEF;
}
static inline int b_voice(int h)
{
    int cls = h >> 5, p = h & 31;
    if (cls == 0) { int place = p / 5, m = p % 5; return m < 4 ? (place * 5 + (m ^ 2)) : UNDEF; }
    if (cls == 1) return (h & ~3) | ((p & 3) ^ 1);      /* slot 0 voiceless fricative <-> 1 voiced fricative */
    return UNDEF;
}
static inline int b_nasal(int h)
{
    int cls = h >> 5, p = h & 31;
    if (cls == 0) return (p / 5) * 5 + 4;
    if (cls == 2) return h | 2;
    return UNDEF;
}
static inline int b_shift(int h)
{
    int cls = h >> 5, p = h & 31;
    if (cls == 0) return p >= 20 ? UNDEF : h + 5;
    if (cls == 1) return p >= 16 ? UNDEF : h + 4;
    if (cls == 2) return p >= 16 ? UNDEF : h + 4;
    return UNDEF;
}
static inline int b_long(int h) { return (h >> 5) == 2 && !(h & 1) ? h | 1 : UNDEF; }

static uint64_t rng_state = 88172645463325252ull;
static uint64_t rng(void) { rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17; return rng_state; }

#define EDGE_DEFS(X) X(0, ASP, asp) X(1, VOICE, voice) X(2, NASAL, nasal) X(3, SHIFT, shift) X(4, LONG, long)

static const int NP[5] = { N_ASP, N_VOICE, N_NASAL, N_SHIFT, N_LONG };
static const uint16_t *IN14[5] = { IN14_ASP, IN14_VOICE, IN14_NASAL, IN14_SHIFT, IN14_LONG };
static const uint16_t *OUT14[5] = { OUT14_ASP, OUT14_VOICE, OUT14_NASAL, OUT14_SHIFT, OUT14_LONG };
static const uint8_t *INH[5] = { INH_ASP, INH_VOICE, INH_NASAL, INH_SHIFT, INH_LONG };
static const uint8_t *OUTH[5] = { OUTH_ASP, OUTH_VOICE, OUTH_NASAL, OUTH_SHIFT, OUTH_LONG };

static int apply_a(int e, int c) { switch (e) { case 0: return a_asp(c); case 1: return a_voice(c); case 2: return a_nasal(c); case 3: return a_shift(c); default: return a_long(c); } }
static int apply_b(int e, int h) { switch (e) { case 0: return b_asp(h); case 1: return b_voice(h); case 2: return b_nasal(h); case 3: return b_shift(h); default: return b_long(h); } }

#define LOOP(BODY) for (long n = 0; n < calls; n++) { int i = (int)(rng() % (uint64_t)np); BODY; }

int main(int argc, char **argv)
{
    if (argc < 5) { fprintf(stderr, "usage: bench_edges <A|B|C> <edge|null> <calls> <setup|full|check>\n"); return 1; }
    char m = argv[1][0];
    const char *q = argv[2];
    long calls = atol(argv[3]);
    const char *mode = argv[4];
    int e = !strcmp(q, "asp") ? 0 : !strcmp(q, "voice") ? 1 : !strcmp(q, "nasal") ? 2 : !strcmp(q, "shift") ? 3 : !strcmp(q, "long") ? 4 : -1;

    /* setup: method C fills its tables from the graph's answer (the pairs) */
    memset(tab, 0xFF, sizeof tab);
    if (m == 'C')
        for (int k = 0; k < 5; k++)
            for (int i = 0; i < NP[k]; i++) tab[k][INH[k][i]] = OUTH[k][i];

    if (!strcmp(mode, "check")) {
        for (int k = 0; k < 5; k++) {
            long bad = 0;
            for (int i = 0; i < NP[k]; i++) {
                int got = m == 'A' ? apply_a(k, IN14[k][i]) : m == 'B' ? apply_b(k, INH[k][i]) : tab[k][INH[k][i]];
                int want = m == 'A' ? OUT14[k][i] : OUTH[k][i];
                bad += got != want;
            }
            printf("parity\t%c\t%s\tpairs=%d\tmismatches=%ld\n", m, k == 0 ? "asp" : k == 1 ? "voice" : k == 2 ? "nasal" : k == 3 ? "shift" : "long", NP[k], bad);
        }
        return 0;
    }
    long sum = 0;
    if (!strcmp(mode, "full")) {
        if (e < 0) { int np = 20; LOOP(sum += i) }                          /* null: loop + rng */
        else {
            int np = NP[e];
            const uint16_t *in14 = IN14[e]; const uint8_t *inh = INH[e]; const uint8_t *t = tab[e];
            if (m == 'A') {
                switch (e) {
                case 0: LOOP(sum += a_asp(in14[i])) break;
                case 1: LOOP(sum += a_voice(in14[i])) break;
                case 2: LOOP(sum += a_nasal(in14[i])) break;
                case 3: LOOP(sum += a_shift(in14[i])) break;
                default: LOOP(sum += a_long(in14[i])) break;
                }
            } else if (m == 'B') {
                switch (e) {
                case 0: LOOP(sum += b_asp(inh[i])) break;
                case 1: LOOP(sum += b_voice(inh[i])) break;
                case 2: LOOP(sum += b_nasal(inh[i])) break;
                case 3: LOOP(sum += b_shift(inh[i])) break;
                default: LOOP(sum += b_long(inh[i])) break;
                }
            } else { LOOP(sum += t[inh[i]]) }
        }
    }
    printf("sum\t%ld\n", sum);
    return 0;
}
