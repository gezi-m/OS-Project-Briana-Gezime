# Paper 1 – Shell Script Analysis & Optimization

10 scripts analyzed, benchmarked, and optimized. Average speedup: 56%.

## Speedup Summary

| Script | Bottleneck | Technique | Speedup |
|--------|-----------|-----------|---------|
| mailformat | 4 redundant sed rules | Single POSIX regex | 25% |
| rn | sed subshell per file | ${var/old/new} | 74% |
| blank_rename | grep+sed per file | Glob + bash substitution | 73% |
| collatz | Fixed 200 iterations | Early exit at h=1 | 60% |
| days_between | basename subprocess | ${##*/} expansion | 60% |
| modular | O(n) brute force | CRT direct formula | O(n)→O(1) |
| mailmerge | sed per recipient | Template cache | ~50% |
| file_organizer | N/A (new script) | All 5 design patterns | Novel |

## Run
```bash
bash tests/generate_test_inputs.sh
bash scripts/mailformat.sh test_email.txt
bash optimized/modular_crt.sh   # outputs: Number = 158 in O(1)
```
