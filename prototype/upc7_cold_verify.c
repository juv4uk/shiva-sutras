/*
 * prototype/upc7_cold_verify.c
 *
 * Independent cold conformance witness for UPC-7 (#33).
 *
 * Deliberately does NOT import or duplicate Python UPC-7 implementation code.
 * It treats upc7-table.tsv as an external machine contract and validates its
 * 7-bit geometry using only the serialized fields.
 *
 * This program is byte-oriented on purpose: UTF-8 spellings in the layout
 * columns are opaque human-boundary payload. They never become code identity.
 */

#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define CELL_COUNT 128
#define FIELD_COUNT 8
#define LINE_CAP 2048
#define SPELLING_CAP 128

static int parse_bits(const char *s, size_t width, unsigned *value) {
    size_t i;
    unsigned out = 0;
    if (strlen(s) != width) {
        return 0;
    }
    for (i = 0; i < width; ++i) {
        if (s[i] != '0' && s[i] != '1') {
            return 0;
        }
        out = (out << 1) | (unsigned)(s[i] - '0');
    }
    *value = out;
    return 1;
}

static int split_tsv(char *line, char *fields[FIELD_COUNT]) {
    size_t count = 1;
    char *p;

    fields[0] = line;
    for (p = line; *p != '\0'; ++p) {
        if (*p == '\t') {
            *p = '\0';
            if (count >= FIELD_COUNT) {
                return 0;
            }
            fields[count++] = p + 1;
        }
    }
    return count == FIELD_COUNT;
}

static void trim_eol(char *line) {
    size_t n = strlen(line);
    while (n > 0 && (line[n - 1] == '\n' || line[n - 1] == '\r')) {
        line[--n] = '\0';
    }
}

static int starts_with(const char *s, const char *prefix) {
    size_t n = strlen(prefix);
    return strncmp(s, prefix, n) == 0;
}

static int fail(size_t line_no, const char *message) {
    fprintf(stderr, "UPC7 cold witness: line %zu: %s\n", line_no, message);
    return 1;
}

static int copy_spelling(char dst[SPELLING_CAP], const char *src, size_t line_no) {
    size_t n = strlen(src);
    if (n >= SPELLING_CAP) {
        fprintf(stderr,
                "UPC7 cold witness: line %zu: spelling field exceeds %d bytes\n",
                line_no, SPELLING_CAP - 1);
        return 0;
    }
    memcpy(dst, src, n + 1);
    return 1;
}

static int check_layout_injective(
    const char values[CELL_COUNT][SPELLING_CAP],
    const char *layout_name
) {
    size_t i, j;
    for (i = 0; i < CELL_COUNT; ++i) {
        if (values[i][0] == '\0') {
            continue;
        }
        for (j = i + 1; j < CELL_COUNT; ++j) {
            if (values[j][0] != '\0' && strcmp(values[i], values[j]) == 0) {
                fprintf(stderr,
                        "UPC7 cold witness: %s spelling %s maps to both %07zu and %07zu\n",
                        layout_name, values[i], i, j);
                return 0;
            }
        }
    }
    return 1;
}

int main(int argc, char **argv) {
    const char *path = argc > 1 ? argv[1] : "upc7-table.tsv";
    const char *expected_header =
        "bits\thex\tclass\tpayload\tstatus\tname\tsa-slp1\tuk";
    const char *class_names[4] = {
        "varga", "non-varga", "vowel", "sign/operator"
    };
    const char *identity_prefixes[4] = {
        "varga.", "non-varga.", "vowel.", "sign."
    };
    FILE *fp;
    char line[LINE_CAP];
    char sa[CELL_COUNT][SPELLING_CAP] = {{0}};
    char uk[CELL_COUNT][SPELLING_CAP] = {{0}};
    size_t row = 0;
    size_t assigned = 0;
    size_t unassigned = 0;

    if (argc > 2) {
        fprintf(stderr, "usage: %s [upc7-table.tsv]\n", argv[0]);
        return 2;
    }

    fp = fopen(path, "rb");
    if (fp == NULL) {
        fprintf(stderr, "UPC7 cold witness: cannot open %s: %s\n",
                path, strerror(errno));
        return 2;
    }

    if (fgets(line, sizeof line, fp) == NULL) {
        fclose(fp);
        return fail(1, "missing TSV header");
    }
    trim_eol(line);
    if (strcmp(line, expected_header) != 0) {
        fclose(fp);
        return fail(1, "unexpected TSV header");
    }

    while (fgets(line, sizeof line, fp) != NULL) {
        char *fields[FIELD_COUNT];
        unsigned code_bits, payload_bits;
        unsigned long hex_value;
        char *end = NULL;
        char expected_hex[8];
        unsigned klass;
        size_t line_no = row + 2;

        if (row >= CELL_COUNT) {
            fclose(fp);
            return fail(line_no, "more than 128 cells");
        }

        if (strchr(line, '\n') == NULL && !feof(fp)) {
            fclose(fp);
            return fail(line_no, "line exceeds verifier buffer");
        }

        trim_eol(line);
        if (!split_tsv(line, fields)) {
            fclose(fp);
            return fail(line_no, "expected exactly 8 TSV fields");
        }

        if (!parse_bits(fields[0], 7, &code_bits)) {
            fclose(fp);
            return fail(line_no, "invalid 7-bit code field");
        }
        if (code_bits != row) {
            fclose(fp);
            return fail(line_no, "code field is not the canonical row identity");
        }

        errno = 0;
        hex_value = strtoul(fields[1], &end, 0);
        if (errno != 0 || end == fields[1] || *end != '\0' || hex_value > 0x7f) {
            fclose(fp);
            return fail(line_no, "invalid hex code field");
        }
        if ((unsigned)hex_value != code_bits) {
            fclose(fp);
            return fail(line_no, "hex and bits encode different cells");
        }
        snprintf(expected_hex, sizeof expected_hex, "0x%02X", code_bits);
        if (strcmp(fields[1], expected_hex) != 0) {
            fclose(fp);
            return fail(line_no, "hex code is not in canonical format");
        }

        klass = code_bits >> 5;
        if (strcmp(fields[2], class_names[klass]) != 0) {
            fclose(fp);
            return fail(line_no, "class does not match the top two code bits");
        }

        if (!parse_bits(fields[3], 5, &payload_bits)) {
            fclose(fp);
            return fail(line_no, "invalid 5-bit payload field");
        }
        if (payload_bits != (code_bits & 0x1f)) {
            fclose(fp);
            return fail(line_no, "payload does not match low five code bits");
        }

        if (strcmp(fields[4], "assigned") == 0) {
            if (fields[5][0] == '\0') {
                fclose(fp);
                return fail(line_no, "assigned cell has no stable machine name");
            }
            if (!starts_with(fields[5], identity_prefixes[klass])) {
                fclose(fp);
                return fail(line_no, "assigned identity name contradicts code class");
            }
            if (starts_with(fields[5], "reserved.")) {
                fclose(fp);
                return fail(line_no, "assigned cell carries reserved identity name");
            }
            ++assigned;
        } else if (strcmp(fields[4], "reserved") == 0) {
            if (!starts_with(fields[5], "reserved.")) {
                fclose(fp);
                return fail(line_no, "unassigned cell lacks reserved.* marker");
            }
            if (fields[6][0] != '\0' || fields[7][0] != '\0') {
                fclose(fp);
                return fail(line_no, "unassigned cell must not render in a human layout");
            }
            ++unassigned;
        } else {
            fclose(fp);
            return fail(line_no, "status must be assigned or reserved/unassigned");
        }

        if (!copy_spelling(sa[row], fields[6], line_no) ||
            !copy_spelling(uk[row], fields[7], line_no)) {
            fclose(fp);
            return 1;
        }

        ++row;
    }

    if (ferror(fp)) {
        fclose(fp);
        fprintf(stderr, "UPC7 cold witness: read error on %s\n", path);
        return 2;
    }
    fclose(fp);

    if (row != CELL_COUNT) {
        return fail(row + 2, "table must contain exactly 128 cells");
    }

    /*
     * #32 established the current geometry count. A later intentional identity
     * assignment must update this independent witness explicitly.
     */
    if (assigned != 107 || unassigned != 21) {
        fprintf(stderr,
                "UPC7 cold witness: expected 107 assigned / 21 unassigned, got %zu / %zu\n",
                assigned, unassigned);
        return 1;
    }

    if (!check_layout_injective(sa, "sa-slp1") ||
        !check_layout_injective(uk, "uk")) {
        return 1;
    }

    printf("UPC7 cold witness OK: 128 cells, 107 assigned, 21 unassigned; "
           "uk/sa-slp1 projections injective\n");
    return 0;
}
