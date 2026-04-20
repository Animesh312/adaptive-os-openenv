# Adaptive OS OpenEnv

### AI-Driven CPU Resource Management Environment

An **OpenEnv-compatible Reinforcement Learning environment** that simulates an **adaptive operating system scheduler** capable of dynamically managing CPU resources based on workload conditions.

The project models **process scheduling, CPU utilization, and queue management** so that an AI agent can learn optimal scheduling decisions.

Built for the **Meta × PyTorch OpenEnv Hackathon**.

---

# Problem

Modern operating systems must efficiently allocate CPU resources across many competing processes.

Poor scheduling decisions lead to:

* High waiting time
* Low CPU utilization
* Process starvation
* Reduced system throughput

This project simulates an **Adaptive Operating System Scheduler** where an AI agent learns to manage CPU resources dynamically.

---

# Key Features

• Adaptive CPU scheduling environment
• Reinforcement learning compatible interface
• Process lifecycle simulation
• Dynamic process queues
• Priority-based scheduling policies
• Resource utilization monitoring
• OpenEnv compatible API

---

# System Architecture

```
                    +--------------------+
                    |    RL Agent / LLM  |
                    |  (Decision Policy) |
                    +---------+----------+
                              |
                              | Action
                              v
                    +--------------------+
                    |    Scheduler Core  |
                    |  Scheduling Logic  |
                    +---------+----------+
                              |
                              | Process Selection
                              v
                +-------------------------------+
                |      Adaptive OS Environment  |
                |                               |
                |  +-------------------------+  |
                |  | Process Queue           |  |
                |  | P1 P2 P3 P4 ...         |  |
                |  +-----------+-------------+  |
                |              |                |
                |              v                |
                |     +---------------+        |
                |     | CPU Execution |        |
                |     | CPU0 CPU1     |        |
                |     +-------+-------+        |
                |             |                |
                |             v                |
                |        System Metrics       |
                |  CPU Usage / Wait Time     |
                +-------------+---------------+
                              |
                              | Reward Signal
                              v
                    +---------------------+
                    | RL Agent Learns     |
                    +---------------------+
```

---

# Environment Design
<h2 align="center">System Architecture</h2>

<p align="center">
<svg width="800" height="420" viewBox="0 0 800 420" xmlns="http://www.w3.org/2000/svg">

<!-- Agent -->
<rect x="320" y="20" width="160" height="60" rx="10" fill="#4CAF50"/>
<text x="400" y="55" font-size="14" fill="white" text-anchor="middle">
RL Agent / Policy
</text>

<!-- Scheduler -->
<rect x="300" y="120" width="200" height="60" rx="10" fill="#2196F3"/>
<text x="400" y="155" font-size="14" fill="white" text-anchor="middle">
Scheduler Core
</text>

<!-- Process Queue -->
<rect x="120" y="230" width="200" height="70" rx="10" fill="#FF9800"/>
<text x="220" y="265" font-size="14" fill="white" text-anchor="middle">
Process Queue
</text>

<!-- CPU -->
<rect x="480" y="230" width="200" height="70" rx="10" fill="#9C27B0"/>
<text x="580" y="265" font-size="14" fill="white" text-anchor="middle">
CPU Execution
</text>

<!-- Metrics -->
<rect x="300" y="340" width="200" height="60" rx="10" fill="#607D8B"/>
<text x="400" y="375" font-size="14" fill="white" text-anchor="middle">
System Metrics
</text>

<!-- Arrows -->

<line x1="400" y1="80" x2="400" y2="120" stroke="black" stroke-width="2"/>
<line x1="400" y1="180" x2="220" y2="230" stroke="black" stroke-width="2"/>
<line x1="400" y1="180" x2="580" y2="230" stroke="black" stroke-width="2"/>

<line x1="220" y1="300" x2="400" y2="340" stroke="black" stroke-width="2"/>
<line x1="580" y1="300" x2="400" y2="340" stroke="black" stroke-width="2"/>

<line x1="400" y1="340" x2="400" y2="80" stroke="black" stroke-width="2" stroke-dasharray="5,5"/>

</svg>
</p>

## State Representation

The agent observes the current system state:

```
cpu_usage
queue_length
process_priority
burst_time
waiting_time
```

Example observation:

```
CPU_USAGE=72%
QUEUE=5
PROCESS_PRIORITY=[1,3,2,4]
```

---

## Action Space

The agent can take the following actions:

```
SCHEDULE      -> execute next process
PRIORITIZE    -> increase process priority
KILL          -> terminate resource-heavy process
```

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

# Build Instructions

Clone repository

```
git clone https://github.com/Animesh312/adaptive-os-openenv
cd adaptive-os-openenv
```

Install dependencies

```
pip install -r requirements.txt
```

---

# Running the Environment

Execute the scheduler agent:

```
python inference.py
```

---

# Example Output

```
[START] task=medium

[STEP] step=1 action=SCHEDULE reward=1.2
[STEP] step=2 action=PRIORITIZE reward=0.9
[STEP] step=3 action=SCHEDULE reward=1.1

[END] task=medium score=0.74 steps=12
```

---

# Scheduler Workflow

```
Process Arrival
      ↓
Process Queue
      ↓
Scheduler Decision
      ↓
CPU Execution
      ↓
System Metrics Updated
      ↓
Reward Generated
      ↓
Agent Learns
```

---

# Use Cases

This environment can be used to study:

• Reinforcement learning for OS scheduling
• Resource allocation strategies
• Multi-agent resource optimization
• AI driven system orchestration

---

# Future Improvements

• Multi-core CPU scheduling
• Memory-aware process management
• GPU resource scheduling
• Visualization dashboard
• Distributed system scheduling

---

# Technologies

Python
OpenEnv Framework
Reinforcement Learning
Docker

---

# Author

Animesh Wankhede

GitHub
https://github.com/Animesh312

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