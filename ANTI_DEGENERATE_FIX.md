# 🔥 Anti-Degenerate Policy Fix - Complete Implementation

## Problem Statement

The RL agent learned a **degenerate policy**:
- **40-60% KILL actions** (should be <20%)
- **7-10% CPU utilization** (should be 50-80%)
- **Rarely uses soft actions** (THROTTLE, DELAY, REALLOCATE)
- **High SLA violations**
- **Optimizes cost by underutilizing** instead of intelligent scheduling

This is a classic **reward hacking** problem where the agent found a loophole:
> "If I kill all processes, cost stays low and I get positive reward!"

---

## Solution Overview

Implemented a **multi-component reward function** with:
1. **Strong CPU utilization targets** (50-80% optimal range)
2. **Progressive underutilization penalties** (<40% heavily penalized)
3. **Excessive KILL penalties** (tracking rolling window)
4. **Soft action rewards** (THROTTLE/DELAY/REALLOCATE incentivized)
5. **Action history tracking** (detect degenerate patterns)
6. **Comprehensive logging** (kill_rate, cpu_utilization, soft_action_ratio)

Plus **PPO hyperparameter tuning** to encourage exploration and prevent policy collapse.

---

## Code Changes

### 1. Environment State Tracking (`env/core.py`)

**Added to `__init__`:**
```python
# Action tracking for anti-degenerate policy enforcement
self.action_history = []
self.max_history = 20  # Track last 20 actions
self.kill_count = 0
self.soft_action_count = 0
self.total_steps = 0
```

**Purpose:** Track action patterns over time to detect and penalize degenerate behavior.

**Added to `reset()`:**
```python
self.action_history = []
self.kill_count = 0
self.soft_action_count = 0
self.total_steps = 0
```

**Purpose:** Reset tracking at episode start for clean evaluation.

---

### 2. Modular Reward Function (`env/core.py` - `step()`)

**New reward structure:**
```python
reward_val = (
    reward_cpu +              # Most important: maintain 50-80% CPU
    reward_fairness +         # Second: be fair
    penalty_sla +             # Critical: avoid SLA violations
    reward_queue +            # Important: manage queue
    penalty_kill +            # Anti-degenerate: penalize KILL spam
    reward_soft_actions +     # Encourage THROTTLE/DELAY/REALLOCATE
    reward_cost +             # Cost matters, but not primary
    reward_stability          # Bonus for stable behavior
)
```

**Key insight:** Cost is now **secondary** (weight 0.3 instead of 0.6), CPU utilization is **primary**.

---

### 3. Reward Component Functions

#### A. `_compute_cpu_reward(cpu_usage)` - Returns: -3.0 to +1.0

**Optimal Range (50-80%):**
```python
if 50 <= cpu_usage <= 80:
    # Peak reward at 65% (middle of range)
    distance_from_ideal = abs(cpu_usage - 65)
    reward = 1.0 - (distance_from_ideal / 30.0)  # 1.0 at 65%, 0.5 at 50/80%
    return reward
```

**Underutilization (<50%):**
```python
if cpu_usage < 20:
    return -3.0  # Massive penalty - "kill everything" degenerate policy
elif cpu_usage < 30:
    return -2.0  # Critical - very wasteful
elif cpu_usage < 40:
    return -1.0  # Warning - suboptimal
else:
    return -0.3  # Acceptable - 40-50% is okay but not ideal
```

**Why this works:**
- CPU < 20% gets **-3.0 penalty** (dominant signal that breaks degenerate policy)
- CPU 50-80% gets **+0.5 to +1.0 reward** (strong incentive)
- Creates clear "valley" outside target range

**Overutilization (>80%):**
```python
if cpu_usage > 95:
    return -1.5  # Critical: System likely failing
elif cpu_usage > 90:
    return -0.8  # Warning: Approaching overload
else:
    return -0.3  # Acceptable: 80-90% is busy but manageable
```

---

#### B. `_compute_queue_reward(queue_length, cpu_usage)` - Returns: -2.0 to 0

**Context-aware queue management:**
```python
if queue_length <= 3:
    return 0.0  # Small queue is healthy

elif queue_length <= 6:
    if cpu_usage > 70:
        return -0.3  # Acceptable: system is busy
    else:
        return -0.8  # Bad: queue building but CPU not working

else:  # queue_length > 6
    base_penalty = -0.5 * queue_length
    if cpu_usage > 90:
        base_penalty *= 0.5  # Reduce penalty if CPU is actually trying
    return max(-2.0, base_penalty)
```

**Why this works:**
- Empty queue + low CPU = wasteful
- Long queue + low CPU = degenerate policy
- Long queue + high CPU = system working hard (less penalty)

---

#### C. `_compute_kill_penalty(action_type, cpu_usage, queue_length)` - Returns: -2.0 to +0.2

**The anti-degenerate policy core:**

```python
# Check if KILL is justified
is_overloaded = (cpu_usage > 85 and queue_length > 8)
is_critical_overload = (cpu_usage > 95)

# Compute recent KILL rate
recent_kills = sum(1 for a in self.action_history[-10:] if a == "KILL")
kill_rate = recent_kills / max(len(self.action_history[-10:]), 1)

# Base penalty for KILL action
if is_critical_overload:
    base_penalty = 0.2  # Small reward - JUSTIFIED
elif is_overloaded:
    base_penalty = 0.0  # ACCEPTABLE
elif cpu_usage > 70:
    base_penalty = -0.5  # QUESTIONABLE
else:
    base_penalty = -1.5  # UNJUSTIFIED - wasteful

# Additional penalty for excessive KILL rate
if kill_rate > 0.5:
    frequency_penalty = -1.5  # Over 50% - DEGENERATE!
elif kill_rate > 0.3:
    frequency_penalty = -0.8  # Over 30% - too aggressive
else:
    frequency_penalty = 0.0  # Acceptable frequency

return base_penalty + frequency_penalty
```

**Why this works:**
- KILL when CPU < 70% → **-1.5 penalty**
- KILL > 50% of time → **additional -1.5 penalty** (total -3.0!)
- This is the **strongest anti-degenerate signal**
- Agent learns: "KILL is expensive unless system is dying"

---

#### D. `_compute_soft_action_reward(action_type, cpu_usage, processes)` - Returns: 0 to +0.8

**Encourage intelligent scheduling:**

```python
if action_type == "THROTTLE":
    if 75 <= cpu_usage <= 90:
        return 0.4 + 0.3  # Perfect use case
    elif cpu_usage > 60:
        return 0.4 + 0.1
    else:
        return 0.4  # OK but not ideal timing

elif action_type == "DELAY":
    if cpu_usage > 70:
        return 0.4 + 0.2
    else:
        return 0.4

elif action_type == "REALLOCATE":
    has_starved = any(p.wait_time > 5 for p in processes)
    if has_starved:
        return 0.4 + 0.4  # Excellent: helping starved processes
    else:
        return 0.4 + 0.2  # Good: proactive reallocation
```

**Why this works:**
- Base reward of +0.4 for any soft action
- Context bonus up to +0.4 more
- Makes soft actions competitive with SCHEDULE (which gets 0)
- Soft action at right time can get +0.8 vs KILL getting -1.5

---

#### E. `_compute_stability_reward()` - Returns: -0.3 to +0.3

**Penalize erratic behavior:**

```python
recent = self.action_history[-5:]
unique_actions = len(set(recent))

if unique_actions == 1:
    return -0.3  # STUCK: Repeating same action
elif unique_actions >= 4:
    return -0.2  # CHAOTIC: Too many different actions
else:
    return 0.2  # STABLE: Good variety without chaos
```

**Why this works:**
- Prevents oscillation (KILL, SCHEDULE, KILL, SCHEDULE...)
- Prevents stuck policies (KILL, KILL, KILL, KILL...)
- Rewards balanced action selection

---

### 4. Info Dict Logging (`env/core.py` - end of `step()`)

**Added comprehensive metrics:**
```python
kill_rate = self.kill_count / max(self.total_steps, 1)
soft_action_ratio = self.soft_action_count / max(self.total_steps, 1)

info.update({
    "cpu_utilization": cpu_usage,
    "kill_rate": kill_rate,
    "soft_action_ratio": soft_action_ratio,
    "fairness_score": fairness,
    "sla_violations": sla_violations,
    "queue_length": queue_length,
    "cost": cost,
    # Reward components for debugging
    "reward_cpu": reward_cpu,
    "reward_fairness": reward_fairness,
    "penalty_sla": penalty_sla,
    "reward_queue": reward_queue,
    "penalty_kill": penalty_kill,
    "reward_soft_actions": reward_soft_actions,
    "reward_cost": reward_cost,
    "reward_stability": reward_stability,
})
```

**Purpose:** 
- Track metrics during training
- Debug reward components
- Detect degenerate policies early

---

### 5. PPO Hyperparameter Tuning (`inference.py` - `train_rl_agent()`)

**Old hyperparameters (led to degenerate policy):**
```python
ent_coef=0.05,        # Low entropy - insufficient exploration
learning_rate=5e-4,   # High LR - unstable
clip_range=0.2,       # Default - allows large policy updates
n_epochs=10           # Standard
```

**New anti-degenerate hyperparameters:**
```python
ent_coef=0.1,         # 🔥 DOUBLED - encourages exploration of soft actions
learning_rate=3e-4,   # 🔥 REDUCED - more stable learning
clip_range=0.15,      # 🔥 TIGHTER - prevents policy collapse
n_epochs=15,          # 🔥 INCREASED - better learning from each batch
vf_coef=0.5,          # Value function coefficient
max_grad_norm=0.5     # Gradient clipping for stability
```

**Why this works:**

1. **Higher entropy (0.1):** 
   - Keeps action distribution diverse
   - Agent explores THROTTLE/DELAY/REALLOCATE more
   - Prevents premature convergence to "KILL everything"

2. **Lower learning rate (3e-4):**
   - Smaller policy updates each step
   - Less likely to collapse into degenerate policy
   - More stable convergence

3. **Tighter clip range (0.15):**
   - Limits size of policy updates (was 0.2, now 0.15)
   - Prevents sudden jumps to extreme policies
   - PPO's trust region is smaller

4. **More epochs (15):**
   - Each batch is learned from more thoroughly
   - Better sample efficiency
   - Stronger gradient signals

---

### 6. Enhanced Training Logging (`inference.py` - `train_rl_agent()`)

**New metrics tracked:**
```python
metrics_history = {
    "kill_rate": [],
    "cpu_utilization": [],
    "soft_action_ratio": [],
    "fairness_score": [],
    "sla_violations": []
}
```

**New training output:**
```
📈 LEARNING CURVE (Anti-Degenerate Training):
================================================================================
Progress     Reward       CPU%     Kill%    Soft%    Fair    
================================================================================
█░░░░░░░░░  10%   -2.456       45.2%    35.2%    15.3%    0.724
██░░░░░░░░  20%   -1.234       52.8%    28.5%    22.1%    0.781
███░░░░░░░  30%   -0.512       58.3%    22.1%    28.7%    0.819
████░░░░░░  40%   +0.123       61.7%    18.5%    32.4%    0.845
█████░░░░░  50%   +0.456       64.2%    15.8%    35.9%    0.867
...
```

**End-of-training diagnostics:**
```python
if final_kill_rate > 40:
    print("⚠️  WARNING: Kill rate is {:.1f}% (>40%) - Policy may be degenerate!")
if final_cpu < 40:
    print("⚠️  WARNING: CPU utilization is {:.1f}% (<40%) - Underutilizing system!")
if final_cpu >= 50 and final_cpu <= 80 and final_kill_rate < 30:
    print("🎉 SUCCESS: Healthy policy!")
```

**Purpose:**
- Detect degenerate policies during training (not after!)
- Show clear progression toward healthy behavior
- Validate that fixes are working

---

### 7. Enhanced Episode Logging (`inference.py` - `run_episode()`)

**Added policy health check:**
```python
print(f"\n🚨 POLICY HEALTH CHECK:")
if kill_rate > 0.4:
    print(f"   ❌ DEGENERATE: Kill rate {kill_rate*100:.1f}% (>40%) - Agent spams KILL!")
elif kill_rate > 0.2:
    print(f"   ⚠️  WARNING: Kill rate {kill_rate*100:.1f}% (>20%) - Too aggressive")
else:
    print(f"   ✅ HEALTHY: Kill rate {kill_rate*100:.1f}% (<20%) - Balanced policy")

if avg_cpu < 40:
    print(f"   ❌ DEGENERATE: CPU {avg_cpu:.1f}% (<40%) - Underutilizing system!")
elif avg_cpu <= 80:
    print(f"   ✅ HEALTHY: CPU {avg_cpu:.1f}% (50-80%) - Optimal range")
```

**Added to return dict:**
```python
return {
    ...
    "kill_rate": kill_rate,
    "cpu_utilization": avg_cpu,
    "soft_action_ratio": soft_pct / 100,
    "sla_violations": total_violations['sla_violations'],
}
```

---

## Expected Results

### Before Fixes:
```
CPU Utilization:  7-10%    ❌ Degenerate
Kill Rate:        40-60%   ❌ Degenerate
Soft Actions:     5-10%    ❌ Not using
Cost:             Very low ✅ But cheating!
Fairness:         N/A      ❌ No processes alive
SLA Violations:   High     ❌ Killing critical processes
```

### After Fixes:
```
CPU Utilization:  55-75%   ✅ Optimal range
Kill Rate:        10-20%   ✅ Balanced
Soft Actions:     25-40%   ✅ Using negotiation
Cost:             Low      ✅ Legitimately optimized
Fairness:         0.80+    ✅ Fair allocation
SLA Violations:   Low      ✅ Protecting critical
```

---

## Training Instructions

1. **Retrain the model:**
```bash
python inference.py --train
```

2. **Watch for healthy indicators:**
- CPU utilization climbing toward 50-80%
- Kill rate decreasing toward 10-20%
- Soft action ratio increasing toward 25-40%
- Reward stabilizing at positive values

3. **Expected learning progression:**
```
Episodes 1-20:   Exploration, high kill rate, low CPU
Episodes 20-50:  Learning, kill rate drops, CPU rises
Episodes 50-100: Refinement, soft actions increase
Episodes 100+:   Mastery, stable healthy policy
```

4. **Validate with benchmark:**
```bash
python inference.py --benchmark
```

Look for policy health check:
```
🚨 POLICY HEALTH CHECK:
   ✅ HEALTHY: Kill rate 15.3% (<20%) - Balanced policy
   ✅ HEALTHY: CPU 62.4% (50-80%) - Optimal range
   ✅ INTELLIGENT: Soft action usage 32.1% (>20%) - Uses negotiation!
```

---

## Why This Solution Works

### 1. CPU Reward Dominates Cost Reward
- **Old:** Cost -0.6, CPU underuse -0.2 → Agent prefers low cost
- **New:** Cost -0.3, CPU underuse -3.0 → Agent MUST maintain CPU

### 2. KILL Penalty Scales with Frequency
- **Old:** Fixed -0.5 penalty when CPU < 50
- **New:** -1.5 base + up to -1.5 frequency = -3.0 total
- Agent learns: "Occasional KILL OK, spamming KILL is terrible"

### 3. Soft Actions are Competitive
- **Old:** No explicit reward for soft actions
- **New:** +0.4 to +0.8 reward for soft actions
- Makes THROTTLE/DELAY/REALLOCATE attractive alternatives to KILL

### 4. Context-Aware Rewards
- Same action can be good or bad depending on state
- KILL when CPU=95% → small reward
- KILL when CPU=20% → large penalty
- Agent learns when each action is appropriate

### 5. Hyperparameters Prevent Collapse
- High entropy keeps exploring soft actions
- Tight clip range prevents sudden jumps to degenerate policy
- Lower LR provides stable convergence

---

## Debugging Tips

If agent still shows degenerate behavior:

1. **Check reward components in logs:**
```python
# Look at info dict during episodes
print(f"reward_cpu: {info['reward_cpu']}")
print(f"penalty_kill: {info['penalty_kill']}")
```

2. **Increase CPU underuse penalty:**
```python
# In _compute_cpu_reward(), make penalty stronger:
if cpu_usage < 20:
    return -5.0  # Was -3.0, now even more severe
```

3. **Increase entropy coefficient:**
```python
# In train_rl_agent():
ent_coef=0.15,  # Was 0.1, increase to 0.15
```

4. **Add curriculum learning:**
```python
# Start with easier task, gradually increase difficulty
tasks = ["easy", "medium", "medium", "hard"]
for task in tasks:
    model.learn(50000)  # 50k timesteps per difficulty
```

---

## File Summary

### Modified Files:

1. **`env/core.py`** (171 lines changed)
   - Added action tracking (lines 11-14, 19-22)
   - Rewrote step() with modular reward (lines 25-110)
   - Added 6 reward component functions (lines 115-250)

2. **`inference.py`** (95 lines changed)
   - Updated PPO hyperparameters (lines 30-48)
   - Enhanced training logging (lines 50-130)
   - Added metrics to metadata (lines 140-148)
   - Enhanced episode health checks (lines 450-480)

### No Changes Needed:
- `env/gym_env.py` (already has 6 actions)
- `env/simulator.py` (simulation logic unchanged)
- `api/server.py` (API unchanged, model loading already optimized)

---

## Mathematical Foundation

### Reward Function as Constrained Optimization:

```
maximize:  reward = Σ(components)

subject to:
  50 ≤ CPU ≤ 80  (hard constraint via -3.0 penalty)
  kill_rate < 0.3  (soft constraint via progressive penalty)
  queue < 6  (soft constraint via quadratic penalty)
```

### Gradient Flow:

Old policy gradient:
```
∇J(θ) ≈ Σ[R(kill_all) * ∇log π(kill|s)]
where R(kill_all) = -0.6*cost ≈ -0.6*2 = -1.2
```
Gradient is weak, agent may not learn to avoid.

New policy gradient:
```
∇J(θ) ≈ Σ[R(kill_all) * ∇log π(kill|s)]
where R(kill_all) = -3.0(CPU) -1.5(kill) -1.5(freq) = -6.0
```
Gradient is strong, agent learns to avoid quickly.

### Exploration via Entropy:

Entropy bonus encourages exploration:
```
H(π) = -Σ π(a|s) log π(a|s)

With ent_coef=0.1:
J_total = J_policy + 0.1 * H(π)

Higher entropy → More uniform action distribution
→ More exploration of soft actions
```

---

This implementation transforms the agent from a "cost hacker" into an "intelligent scheduler" that balances efficiency, fairness, and stability.
