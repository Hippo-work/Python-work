#define WORD uint64_t
WORD S = ~0, mask[256];
for (int j = 0; j < m; j++) mask[P[j]] &= ~(1ULL << j);
for (int i = 0; i < n; i++) {
    S = (S << 1) | mask[T[i]];
    if (~S & (1ULL << m)) { /* Match at i - m + 1 */ }
}