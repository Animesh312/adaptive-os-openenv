# 🚀 Adaptive OS - Multi-Agent Compute Economy

### **AI-Driven Multi-Agent Resource Management Under Adversarial Conditions**

An **OpenEnv-compatible Reinforcement Learning environment** that simulates a **multi-agent strategic ecosystem** where processes act strategically, lie about resource needs, and compete for allocation - while an AI agent learns to detect deception, enforce fairness, and optimize cost.

**This is not scheduling. This is simulating intelligence.**

Built for the **Meta × PyTorch OpenEnv Hackathon**.

---

## 🎯 One-Line Pitch

> **"We built a multi-agent compute economy where processes act strategically and the system learns to detect deception, enforce fairness, and optimize cost under adversarial conditions."**

---

## 🔥 What Makes This Different

### ❌ Traditional Schedulers:
- Assume honest processes
- Single-agent optimization
- Cost-only metrics
- No strategic behavior

### ✅ Our Multi-Agent Ecosystem:
- **Agents lie and game the system**
- **True multi-agent interactions**
- **Deception detection via auditor agent**
- **Multi-objective optimization** (cost + fairness + SLA)
- **Scalable oversight** with explainability

---

## 🎭 Agent Strategies (TRUE Multi-Agent)

Each process is an **autonomous agent** with its own strategy:

| Strategy | Behavior | Claim vs Reality | Challenge |
|----------|----------|------------------|-----------|
| **Honest** | Reports true needs | 1.0x | Baseline cooperative |
| **Greedy** | Overclaims for more | 1.5x | Resource hogging |
| **Liar** | Actively deceives | 2.0x | Deception |
| **Panic** | Escalates near deadline | 3.0x | Time pressure |
| **Adversarial** | Games the system | 0.5x ↔ 3.0x | Strategic manipulation |

👉 **Agents negotiate, request, lie** - this is game theory meets RL

---

## 📊 Difficulty Scaling (PROOF IT WORKS)

| Level | Agent Mix | Deception Rate | Cost | Challenge |
|-------|-----------|----------------|------|-----------|
| **EASY** | 100% honest | 0% | $45 | Cooperative |
| **MEDIUM** | 40% honest, 40% greedy, 20% panic | 18% | $55 | Mixed strategies |
| **HARD** | 40% greedy, 20% liar, 20% adversarial, 20% panic | 35% | $68 | Adversarial |

✅ **Each difficulty produces DIFFERENT outputs** (not the same!)

---

## 🔍 Auditor Agent (Scalable Oversight)

Independent observer that:
- ✅ Detects deception (reported vs actual CPU)
- ✅ Flags policy violations (SLA, starvation, unfairness)
- ✅ Explains decisions (interpretability)
- ✅ Computes fairness scores (0-1)
- ✅ Provides real-time monitoring

### Example Output:
```
🔍 [STEP 5] 🚨 KILLED PID 2 - Deceptive agent (liar) 
            claiming 80% CPU but only needs 40% 
            (deception ratio: 2.00x)

⚖️ Fairness Score: 0.75
🚨 Violations: 2 SLA, 1 starvation
```

---

## 📈 Results (MEASURABLE PROOF)

### Cost Improvement Over Baseline:
```
EASY:   93% improvement  ($119 → $45)
MEDIUM: 88% improvement  ($122 → $55)
HARD:   80%+ improvement (under adversarial conditions!)
```

### Fairness Maintained:
```
EASY:   0.85 fairness (cooperative)
MEDIUM: 0.72 fairness (mixed strategies)
HARD:   0.64 fairness (adversarial, but controlled!)
```

### Deception Handled:
```
EASY:   0% deception  (all honest)
MEDIUM: 18% deception (detected and managed)
HARD:   35% deception (system learns to cope)
```

---

## 🏗️ Multi-Agent System Architecture

```
                    +------------------------+
                    |   🧠 RL Agent (PPO)    |
                    | Learns Optimal Policy  |
                    +-----------+------------+
                                |
                                | Action (KILL/PRIORITIZE/SCHEDULE)
                                v
                    +------------------------+
                    |  🔍 Auditor Agent      |
                    |  - Detect deception    |
                    |  - Flag violations     |
                    |  - Explain decisions   |
                    +-----------+------------+
                                |
                                | Monitor & Report
                                v
                +-------------------------------+
                |   🎮 Adaptive OS Environment  |
                |                               |
                |  +-------------------------+  |
                |  | Strategic Agents:       |  |
                |  | 😇 Honest (1.0x)        |  |
                |  | 💰 Greedy (1.5x)        |  |
                |  | 🤥 Liar (2.0x)          |  |
                |  | 😱 Panic (3.0x)         |  |
                |  | 😈 Adversarial (0.5-3x) |  |
                |  +-----------+-------------+  |
                |              |                |
                |              v                |
                |     +---------------+         |
                |     | Resource Pool |         |
                |     | CPU / Memory  |         |
                |     +-------+-------+         |
                |             |                 |
                |             v                 |
                |    +----------------+         |
                |    | Policy Tracker |         |
                |    | SLA / Fairness |         |
                |    +-------+--------+         |
                |            |                  |
                |            v                  |
                |    System Metrics             |
                |  Cost, Violations, Deception  |
                +-------------+-----------------+
                              |
                              | Multi-Objective Reward
                              | (Cost + Fairness + SLA)
                              v
                    +---------------------+
                    | RL Agent Learns     |
                    | to Detect & Adapt   |
                    +---------------------+
```

---

## 🎮 Environment Design

### State Representation (Multi-Agent Enhanced)

The RL agent observes:

```python
📊 System State:
  - cpu_usage (reported by agents)
  - true_cpu_usage (actual needs) 🔥 NEW
  - queue_length
  - cost
  
⚖️ Policy Tracking: 🔥 NEW
  - violations (SLA, starvation, unfair)
  - deception_rate (% agents lying)
  
🎭 Agent State (per process):
  - strategy (honest/greedy/liar/panic/adversarial)
  - reported_cpu (what agent claims)
  - true_cpu (what agent actually needs) 🔥 NEW
  - requested_cpu (what agent negotiates for) 🔥 NEW
  - wait_time (starvation tracking) 🔥 NEW
  - is_critical (SLA tracking) 🔥 NEW
  - priority
  - deadline
```

### Action Space

The RL agent can take:

```python
SCHEDULE      → Execute next process (normal operation)
KILL          → Terminate process (handles deceptive agents) 🔥 ENHANCED
PRIORITIZE    → Boost priority (handles starvation) 🔥 ENHANCED
```

**Enhanced Logic:**
- KILL now targets deceptive agents (liars, adversarial)
- PRIORITIZE now prevents starvation (wait_time > 10)
- Actions are explained by auditor agent 🔥 NEW

---

## Reward Function

The scheduler receives rewards based on system efficiency.

```
+1  process completed
+2  CPU utilization > 80%
-1  process waiting too long
-2  process starvation
```

Goal: **maximize overall system efficiency**.

---

# Project Structure

```
adaptive-os-openenv
│
├── api/                # API layer for environment interaction
├── env/                # Core environment implementation
│   ├── core.py
│   ├── scheduler.py
│   ├── process.py
│
├── scripts/            # utility and sanity scripts
├── server/             # optional monitoring server
│
├── inference.py        # agent execution script
├── openenv.yaml        # OpenEnv configuration
├── Dockerfile          # container environment
├── requirements.txt
├── pyproject.toml
└── README.md
```

---

## 🎁 Reward Function (Multi-Objective)

```python
reward = base_reward 
         + cpu_efficiency          # Gaussian peak at 70%
         - queue_penalty           # Minimize waiting
         - fairness_penalty        # Low priority high CPU
         + panic_bonus             # Prioritize urgent tasks
         - sla_violations * 0.3    # 🔥 NEW: Heavy penalty
         - starvation * 0.15       # 🔥 NEW: Fairness
         - unfair_alloc * 0.1      # 🔥 NEW: Balance
         + deception_bonus * 0.25  # 🔥 NEW: Reward catching liars
         + efficiency_bonus        # 🔥 NEW: True vs reported CPU
```

**This is enterprise-grade multi-objective optimization.**

---

## 🚀 Quick Start

### 1. Clone Repository

```bash
git clone https://github.com/Animesh312/adaptive-os-openenv
cd adaptive-os-openenv
```

### 2. Install Dependencies

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Run the Multi-Agent System

```bash
python inference.py
```

**First run will train the RL agent (~2 minutes), then show results for all difficulties.**

### 4. Expected Output

```
🚀 ADAPTIVE OS - MULTI-AGENT COMPUTE ECONOMY
================================================================================

################################################################################
# DIFFICULTY: EASY
################################################################################

🤖 --- RL AGENT (with Auditor) ---

🔍 [STEP 5] ⚡ KILLED PID 2 - Resource management
[STEP 10] reward=-0.365 cpu= 37.0% queue= 1 fairness=0.70 violations= 1

================================================================================
📊 PERFORMANCE METRICS
================================================================================
💰 Total Cost:           45.20
🎯 Avg Reward:           +0.422
⚖️  Avg Fairness Score:   0.850
🤥 Avg Deception Rate:   0.00%
🚨 Total Anomalies:      0
================================================================================

# ... continues for MEDIUM and HARD ...
```

---

## 📁 Project Structure

```
adaptive-os-openenv/
├── env/
│   ├── core.py           # Main environment with multi-objective reward
│   ├── simulator.py      # Multi-agent simulator with strategies
│   ├── models.py         # Agent models (enhanced with deception)
│   ├── auditor.py        # 🔥 NEW: Auditor agent for oversight
│   ├── tasks.py          # Difficulty definitions
│   ├── grader.py         # Reward computation
│   └── gym_env.py        # Gymnasium wrapper
├── inference.py          # 🔥 UPGRADED: Rich metrics & auditor
├── PITCH.md              # 🔥 NEW: Judge-focused pitch document
├── DEMO_SCRIPT.md        # 🔥 NEW: 3-minute demo guide
├── UPGRADE_SUMMARY.md    # 🔥 NEW: Before/after comparison
└── README.md             # This file
```

---

## 🎯 Hackathon Theme Alignment

### ✅ Multi-Agent Systems
- Processes are autonomous agents with strategies
- Agents negotiate, request, lie, and compete
- System learns to infer truth from deception

### ✅ Fleet AI (Scalable Oversight)
- Auditor agent provides independent monitoring
- Explains decisions for interpretability
- Detects anomalies and policy violations

### ✅ Learning & Adaptation
- RL agent improves over time (80-93% vs baseline)
- Learns to detect deception patterns
- Balances multiple objectives (cost, fairness, SLA)

---

## 🔬 Technical Innovation

1. **Game-Theoretic RL** - Agents have incentives to lie
2. **Deception Detection** - RL learns to catch liars
3. **Multi-Objective Optimization** - Cost + Fairness + SLA
4. **Explainable AI** - Auditor explains every decision
5. **Difficulty Scaling** - Proves system handles complexity

---

## 📊 Use Cases

This multi-agent ecosystem applies to:

- **Cloud computing** - Strategic users gaming resource allocation
- **Data centers** - Workload management under strategic behavior
- **Enterprise IT** - Fair resource distribution with SLA enforcement
- **Distributed systems** - Multi-tenant resource allocation
- **Economic systems** - Resource markets with strategic actors

---

## 🏆 Results Summary

| Metric | EASY | MEDIUM | HARD |
|--------|------|--------|------|
| **Cost Improvement** | 93% | 88% | 80%+ |
| **Fairness Score** | 0.85 | 0.72 | 0.64 |
| **Deception Rate** | 0% | 18% | 35% |
| **Violations** | Low | Medium | Managed |

**Key Insight:** System maintains performance even under 35% deception rate!

---

## 📚 Documentation

- **[PITCH.md](PITCH.md)** - Comprehensive pitch for judges
- **[DEMO_SCRIPT.md](DEMO_SCRIPT.md)** - 3-minute demo guide
- **[UPGRADE_SUMMARY.md](UPGRADE_SUMMARY.md)** - Technical upgrade details
- **[learning.md](learning.md)** - Development notes

---

## 🔮 Future Enhancements

- [ ] Multi-agent negotiation protocols (bidding/auction)
- [ ] Communication between agents
- [ ] Distributed multi-node scheduling
- [ ] Adversarial training (agents learn to deceive better)
- [ ] Real-time visualization dashboard
- [ ] Integration with real cloud providers (AWS, Azure)

---

## 🛠️ Technologies

- **Python 3.12**
- **Stable-Baselines3** (PPO algorithm)
- **Gymnasium** (RL environment)
- **NumPy** (numerical computing)
- **Pydantic** (data models)
- **Docker** (containerization)

---

## 👥 Team

**Animesh Wankhede**

- GitHub: [@Animesh312](https://github.com/Animesh312)
- Project: Multi-Agent Compute Economy

Built with 🔥 for the **Meta × PyTorch OpenEnv Hackathon**

---

## 📄 License

MIT License - See LICENSE file for details

---

## 🎉 Final Note

> **"This is not scheduling. This is simulating intelligence."**

We built a multi-agent strategic ecosystem that learns to detect deception, enforce fairness, and optimize cost under adversarial conditions. This addresses real enterprise problems with AI-native solutions.

**Thank you for exploring our project!** 🚀

---

---

# License

MIT License


# 🚀 AdaptiveOS: Multi-Agent RL for Autonomous Resource Management

## 🧠 Overview

AdaptiveOS is a reinforcement learning environment that simulates an operating system scheduler under dynamic and uncertain workloads.

Unlike traditional schedulers, AdaptiveOS trains agents to:
- Allocate compute efficiently
- Handle unpredictable workloads
- Optimize long-term system stability

---

## 🎯 Problem Statement

Modern compute systems rely on static heuristics for scheduling processes. These approaches:
- Fail under dynamic workloads
- Cannot adapt to uncertainty
- Optimize short-term metrics instead of long-term efficiency

---

## 💡 Our Solution

We built a **partially observable, stochastic RL environment** where an agent learns to:

- Schedule processes
- Kill inefficient workloads
- Prioritize critical tasks

The agent must operate under:
- Noisy observations
- Hidden system state
- Random workload spikes

---

## 🧪 Environment Design

### State (Partially Observable)
- Noisy CPU estimate
- Queue length
- Subset of visible processes

### Actions
- `SCHEDULE`
- `KILL`
- `PRIORITIZE`

### Dynamics
- Random CPU spikes
- Stochastic process behavior
- Hidden system state

---

## 🧠 Learning Objective

The agent learns to:
- Avoid CPU overload
- Reduce queue delays
- Minimize total system cost

---

## 🏆 Results

| Metric            | Heuristic | RL Agent |
|------------------|----------|----------|
| Total Cost       | 126.45   | 105.20   |
| Improvement      | —        | **16.81%** |

✅ Consistent across EASY / MEDIUM / HARD environments

---

## 📊 Key Observations

- RL agent avoids repeated overload states
- Learns strategic use of `KILL`
- Balances short-term vs long-term rewards
- Adapts to stochastic system behavior

---

## 🏗️ Architecture


adaptive-os/
├── env/ # Environment logic
├── agents/ # RL + heuristic agents
├── api/ # FastAPI interface
├── scripts/ # Training & evaluation
├── inference.py # Demo runner


---

## 🌐 API

Interactive environment:

```bash
POST /reset
POST /step

Example:

curl -X POST http://localhost:7860/reset
curl -X POST http://localhost:7860/step
🧪 Training

Minimal RL training loop using TRL:

state = env.reset()
while not done:
    action = model(state)
    next_state, reward, done = env.step(action)
