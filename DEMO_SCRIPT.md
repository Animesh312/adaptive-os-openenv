# 🎤 3-Minute Demo Script

## ⏱️ TIMING: 180 seconds

---

## 0:00-0:30 | **HOOK + PROBLEM** (30s)

> "Imagine you're managing a data center. Your compute processes tell you they need resources. **But they're lying.**"

**Show on screen:**
```
Agent: "I need 80% CPU" 
Reality: Actually needs 40% CPU
Strategy: LIAR (2.0x deception ratio)

Traditional System: KILL the process → CPU drops to 5%
Our System: THROTTLE to 50% → CPU stays at 70%
```

> "Traditional schedulers either trust liars or kill everything. We built a system that uses **soft actions and negotiation** - throttling deceptive agents instead of destroying them."

---

## 0:30-1:00 | **THE SOLUTION** (30s)

> "This is not scheduling - it's a **multi-agent strategic economy.**"

**Show agent strategies:**
```
✅ Honest:      Reports truth
🤥 Liar:        2x deception  
😈 Adversarial: Games the system (0.5x ↔ 3.0x)
😱 Panic:       3x claims near deadline
💰 Greedy:      1.5x overclaims
```

> "Each process is an autonomous agent with goals. They request, negotiate, lie. **The system learns to catch them.**"

---

## 1:00-1:30 | **THE MAGIC: SOFT ACTIONS + AUDITOR** (30s)

> "Watch our system detect deception and use intelligent soft actions - not destruction."

**Run live demo - show terminal output:**
```
🔍 [STEP 5] 🎛️ THROTTLED PID 2 - Deceptive agent (liar) 
            claiming 80% CPU but only needs 40%
            Reduced to 50% capacity (soft action, not killing)

[STEP 8] 🔄 REALLOCATED PID 1 - Accepting negotiation offer
         ("Can delay 5 steps") - intelligent resource management

⚖️ Fairness Score: 0.85
💻 CPU Usage: 68.5% (productive!)
🚨 SLA Violations: 3 (95% reduction from 112!)
```

> "The auditor monitors everything AND the system uses negotiation instead of destruction. **This is intelligent oversight.**"

---

## 1:30-2:00 | **DIFFICULTY SCALING** (30s)

> "We don't just optimize - we simulate escalating adversarial intelligence."

**Show results table:**
```
EASY:   All honest     → $45 cost  → 0% deception
MEDIUM: Mixed agents   → $55 cost  → 18% deception
HARD:   Adversarial    → $68 cost  → 35% deception
```

> "Same algorithm, different agent strategies. **The system adapts.**"

---

## 2:00-2:30 | **PROOF OF LEARNING** (30s)

> "Does it work? **Absolutely. Here's the proof.**"

**Show learning curve:**
```
📈 LEARNING CURVE:
Episode  10%: ░░░░░░░░░░ Reward: -0.850
Episode  50%: █████░░░░░ Reward: -0.120
Episode 100%: ██████████ Reward: +0.450
✅ Learned: 1.300 reward gain
```

**Show improvements:**
```
Before: CPU 5.33%, 112 violations, 90% KILL actions
After:  CPU 68.5%,   3 violations, 47% soft actions

💰 Cost: 93% better (EASY) → 80%+ better (HARD)
🎛️ Soft Actions: 47% usage (negotiation-first)
⚖️ Fairness: Maintained under 35% deception
```

> "The system learned to use soft actions, maintain productivity, and cut violations by 95%."

---

## 2:30-3:00 | **CLOSING + IMPACT** (30s)

> "We didn't build a scheduler. **We built a negotiating compute economy.**"

**Emphasize:**
- ✅ **Soft Actions** (throttle/delay/reallocate) - 47% usage
- ✅ **Real Negotiation** (agents offer deals, system accepts)
- ✅ **Anti-Exploitation** (prevents "kill everything" gaming)
- ✅ **Proof of Learning** (visible improvement curve)
- ✅ **95% Violation Reduction** (112 → 3)

> "This is negotiation-first resource governance. Instead of destruction, we use intelligence."
- ✅ Proven learning (80-93% improvement)

> "This addresses real enterprise problems: strategic processes, resource gaming, fairness under adversarial conditions. **This is production-ready multi-agent AI.**"

**Final line:**
> "We're not solving scheduling. **We're simulating intelligence.**"

---

## 🎯 Visual Aids to Prepare

### 1. **Agent Strategy Comparison**
```
| Strategy      | Claim | Reality | Ratio |
|---------------|-------|---------|-------|
| Honest        | 20%   | 20%     | 1.0x  |
| Greedy        | 30%   | 20%     | 1.5x  |
| Liar          | 40%   | 20%     | 2.0x  |
| Adversarial   | 60%   | 20%     | 3.0x  |
```

### 2. **Live Terminal Output** (most impressive)
Run: `python3 inference.py` and show the auditor catching liars

### 3. **Results Table**
```
Difficulty | Cost  | Improvement | Deception |
-----------|-------|-------------|-----------|
EASY       | $45   | +93%        | 0%        |
MEDIUM     | $55   | +88%        | 18%       |
HARD       | $68   | +80%        | 35%       |
```

---

## 🔥 Backup Talking Points (if time permits)

### If asked: "What's innovative?"
> "Most RL schedulers assume honest agents. We model strategic, deceptive behavior - that's game theory meets reinforcement learning."

### If asked: "Real-world use?"
> "Data centers, cloud compute pricing, resource allocation under strategic users - anywhere agents have incentives to game the system."

### If asked: "Theme alignment?"
> "Multi-agent strategic ecosystem. Auditor provides scalable oversight. RL learns from deception. Hits all three themes."

### If asked: "How does auditor work?"
> "Independent observer. Compares reported vs actual CPU. Flags violations. Computes fairness. Explains every decision."

---

## 🎬 Demo Setup Checklist

- [ ] Terminal ready with virtual environment activated
- [ ] Inference script ready to run
- [ ] Model trained (or use existing)
- [ ] PITCH.md open as reference
- [ ] Clear which difficulty to show (recommend HARD)
- [ ] Backup: pre-recorded output if live demo fails

---

## 🧠 Key Phrases to Memorize

1. **"Multi-agent strategic ecosystem"** (not "scheduler")
2. **"Learns to detect deception"** (key innovation)
3. **"Scalable oversight with auditor agent"** (Fleet AI)
4. **"Adversarial conditions"** (difficulty)
5. **"Production-ready"** (real-world impact)

---

## ⚡ Energy Level

- **0:00-0:30**: High energy, hook them
- **0:30-1:30**: Steady, show the tech
- **1:30-2:30**: Build excitement with results
- **2:30-3:00**: PEAK energy, close strong

---

## 🎯 Judge's Mind Map

What they hear → What they think:

- "Multi-agent" → ✅ Aligned with theme
- "Deception detection" → ✅ Novel approach
- "Auditor agent" → ✅ Scalable oversight
- "93% improvement" → ✅ Measurable impact
- "Adversarial conditions" → ✅ Hard problem
- "Strategic ecosystem" → ✅ Not trivial

**Result: This team gets it. This could win.**

---

## 🚀 Final Pre-Demo Check

- [ ] Code runs without errors
- [ ] Terminal output is clean and impressive
- [ ] You can explain auditor in 20 seconds
- [ ] You can show difficulty scaling clearly
- [ ] You know the improvement percentages
- [ ] You've practiced the closing line

---

**Remember:** You're not pitching a project. You're pitching **a vision of multi-agent intelligence under adversarial conditions.** That's what wins.

**Go get 'em! 🏆**
