/* Design-level cost of three queries on the 7-bit prototypes (research; I refs via Cachegrind).
 *
 *   savarna(a, b)      1.1.9
 *   in_ac(x)           pratyahara ac
 *   in_jhal(x)         pratyahara jhal
 *
 * Designs: H hand table, D derived (saṅkṣepa7), V varṇa7 are GEOMETRY (the answer is read from the bits by a rule);
 * A akṣara7, T tantu7, L legacy are ORDINALS (the cell is an index: the answer needs a table or an interval).
 * Usage: bench7 <H|D|V|A|T|L> <query: sav|ac|jhal|null> <calls> <mode: setup|full|check>
 */
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "tables.h"

static const uint8_t *cells;
static int geometry;
static uint64_t sav_row[128];            /* ordinals: savarna as a bit row per cell (built in setup) */
static uint64_t jhal_lo, jhal_hi;        /* membership mask over cells 0..127 (built in setup, all designs) */
static int ac_lo, ac_hi, ac_contig;

static inline int effort(int kind) { return kind >> 1; }          /* kind 0,1 = ushma (0), 2,3 = ishat (1) */

static inline int sav_geometry(int a, int b)
{
    int ca = a >> 5, cb = b >> 5;
    if (ca != cb) return 0;
    int pa = a & 31, pb = b & 31;
    switch (ca) {
    case 0: return pa / 5 == pb / 5;
    case 1: return (pa >> 2) == (pb >> 2) && effort(pa & 3) == effort(pb & 3);
    case 2: return (pa >> 2) == (pb >> 2);
    default: return 0;
    }
}

static inline int sav_ordinal(int a, int b) { return (int)((sav_row[a] >> b) & 1); }

static inline int ac_geometry(int x) { return (x >> 5) == 2 && ((x >> 2) & 7) < 7; }   /* vowel class, Sanskrit rows */
static inline int ac_interval(int x) { return x >= ac_lo && x <= ac_hi; }

static inline int jhal_mask(int x) { return (int)(((x < 64 ? jhal_lo >> x : jhal_hi >> (x - 64))) & 1); }

static uint64_t rng_state = 88172645463325252ull;
static uint64_t rng(void) { rng_state ^= rng_state << 13; rng_state ^= rng_state >> 7; rng_state ^= rng_state << 17; return rng_state; }

int main(int argc, char **argv)
{
    if (argc < 5) { fprintf(stderr, "usage: bench7 <H|D|V|A|T|L> <sav|ac|jhal> <calls> <setup|full|check>\n"); return 1; }
    char d = argv[1][0];
    const char *q = argv[2];
    long calls = atol(argv[3]);
    const char *mode = argv[4];
    switch (d) {
    case 'H': cells = CELL_H; geometry = 1; ac_lo = AC_LO_H; ac_hi = AC_HI_H; ac_contig = AC_CONTIGUOUS_H; break;
    case 'D': cells = CELL_D; geometry = 1; ac_lo = AC_LO_D; ac_hi = AC_HI_D; ac_contig = AC_CONTIGUOUS_D; break;
    case 'V': cells = CELL_V; geometry = 1; ac_lo = AC_LO_V; ac_hi = AC_HI_V; ac_contig = AC_CONTIGUOUS_V; break;
    case 'A': cells = CELL_A; ac_lo = AC_LO_A; ac_hi = AC_HI_A; ac_contig = AC_CONTIGUOUS_A; break;
    case 'T': cells = CELL_T; ac_lo = AC_LO_T; ac_hi = AC_HI_T; ac_contig = AC_CONTIGUOUS_T; break;
    default:  cells = CELL_L; ac_lo = AC_LO_L; ac_hi = AC_HI_L; ac_contig = AC_CONTIGUOUS_L; break;
    }

    /* setup: the tables a design needs (ordinal savarna rows, the jhal mask) */
    memset(sav_row, 0, sizeof sav_row);
    if (!geometry)
        for (int i = 0; i < NSOUNDS; i++)
            for (int j = 0; j < NSOUNDS; j++)
                if ((ORACLE_SAVARNA[i] >> j) & 1) sav_row[cells[i]] |= 1ULL << cells[j];
    jhal_lo = jhal_hi = 0;
    for (int i = 0; i < NSOUNDS; i++)
        if ((ORACLE_JHAL >> i) & 1) { if (cells[i] < 64) jhal_lo |= 1ULL << cells[i]; else jhal_hi |= 1ULL << (cells[i] - 64); }

    if (strcmp(mode, "check") == 0) {
        long bad_sav = 0, bad_ac = 0, bad_jhal = 0;
        for (int i = 0; i < NSOUNDS; i++) {
            for (int j = 0; j < NSOUNDS; j++) {
                int got = geometry ? sav_geometry(cells[i], cells[j]) : sav_ordinal(cells[i], cells[j]);
                bad_sav += got != (int)((ORACLE_SAVARNA[i] >> j) & 1);
            }
            int ac = geometry ? ac_geometry(cells[i]) : (ac_contig ? ac_interval(cells[i]) : -1);
            bad_ac += ac != (int)((ORACLE_AC >> i) & 1);
            bad_jhal += jhal_mask(cells[i]) != (int)((ORACLE_JHAL >> i) & 1);
        }
        printf("parity\t%c\tsavarna_mismatches=%ld/1764\tac_mismatches=%ld/42\tjhal_mismatches=%ld/42\n", d, bad_sav, bad_ac, bad_jhal);
        return 0;
    }
    long sum = 0;
    if (strcmp(mode, "full") == 0) {
        for (long n = 0; n < calls; n++) {
            int i = (int)(rng() % NSOUNDS), j = (int)(rng() % NSOUNDS);
            if (!strcmp(q, "sav")) sum += geometry ? sav_geometry(cells[i], cells[j]) : sav_ordinal(cells[i], cells[j]);
            else if (!strcmp(q, "null")) sum += i + j;                      /* loop + rng overhead */
            else if (!strcmp(q, "ac")) sum += geometry ? ac_geometry(cells[i]) : ac_interval(cells[i]);
            else sum += jhal_mask(cells[i]);
        }
    }
    printf("sum\t%ld\n", sum);
    return 0;
}
