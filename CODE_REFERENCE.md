# 🔥 Code Reference: Anti-Degenerate Policy

## Core Functions at a Glance

### 1. CPU Reward (-3.0 to +1.0)
```python
if 50 <= cpu <= 80: return 1.0 - abs(cpu-65)/30
if cpu < 20: return -3.0  # Breaks degenerate policy
if cpu < 30: return -2.0
if cpu < 40: return -1.0
else: progressive penalties
```

### 2. KILL Penalty (-3.0 to +0.2)
```python
base = -1.5 if cpu < 70 else 0.0
frequency = -1.5 if kill_rate > 50% else 0.0
return base + frequency  # Up to -3.0 total
```

### 3. Soft Action Reward (0 to +0.8)
```python
base = 0.4 for THROTTLE/DELAY/REALLOCATE
bonus = up to +0.4 based on context
return base + bonus
```

### 4. PPO Config
```python
ent_coef=0.1         # High exploration
learning_rate=3e-4   # Stable convergence
clip_range=0.15      # Prevent collapse
n_epochs=15          # Better learning
```

---

## Expected Learning Progression

```
Episodes 1-20:    CPU rises from 10% to 40%
                  Kill rate drops from 60% to 40%

Episodes 20-50:   CPU reaches 50-60%
                  Kill rate drops to 25-30%
                  Soft actions increase to 20%

Episodes 50-100:  CPU stabilizes at 55-70%
                  Kill rate drops to 15-20%
                  Soft actions reach 30-35%

Episodes 100+:    Healthy policy maintained
```

---

## Target Metrics

| Metric | Before | After |
|--------|--------|-------|
| CPU | 7-10% | 50-80% |
| Kill Rate | 40-60% | 10-20% |
| Soft Actions | 5-10% | 25-40% |

---

## Commands

```bash
# Train
python inference.py --train

# Benchmark
python inference.py --benchmark

# Demo
python inference.py
```
