# Paper 3 – MLFQ Scheduling Optimization

## Requirements
```bash
pip install numpy matplotlib scipy
```

## Quick Run
```bash
cd simulation
python3 mlfq_simulate.py --n 300 --m 100 --q1 8 --q2 16 --l1 30 --l2 30 --trials 15
```

## Full Reproduction (~15-30 min)
```bash
cd simulation
python3 run_all.py
```

## Key Results
| Criterion | Optimal Q1 | Optimal Q2 | Value |
|-----------|-----------|-----------|-------|
| Max Throughput | 20ms | 32ms | 0.0020 proc/ms |
| Min Response Time | 4ms | 4ms | 782ms |
| Best T% (SJF) | — | — | 70-90% |

Exponential burst distribution yields 2.6x higher throughput than Uniform.
M/M/S analysis: S=3 provides 8.75x queue length reduction vs S=2.
