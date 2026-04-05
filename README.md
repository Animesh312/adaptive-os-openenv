# Adaptive OS OpenEnv Environment

## Overview

This project implements a real-world OpenEnv environment simulating an adaptive operating system scheduler.

The agent must dynamically manage CPU usage, process scheduling, and system load under varying conditions.

---

## Motivation

Modern operating systems must handle:
- CPU load balancing
- Process prioritization
- Queue management under dynamic workloads

This environment models these real-world challenges for evaluating AI agents.

---

## Environment Design

### State (Observation)

- CPU usage (%)
- Memory usage (%)
- Active processes (PID, CPU, memory, priority)
- Queue length
- Timestep

---

### Actions

- `SCHEDULE` → allocate CPU
- `KILL` → terminate process
- `PRIORITIZE` → adjust priority

---

## Tasks

### Easy
- Goal: Maintain stable CPU (~70%)
- Focus: Basic system stability

### Medium
- Goal: Balance CPU + queue
- Focus: Latency and throughput tradeoff

### Hard
- Goal: Handle overload conditions
- Focus: Stability + backlog + penalties

---

## Reward Design

- Continuous reward (0.0–1.0)
- Encourages:
  - Stable CPU
  - Low queue length
- Penalizes:
  - Overload (CPU > 95%)
  - High backlog
  - Inefficient scheduling

---

## Difficulty Progression

The difficulty progression ensures monotonic performance degradation:

easy > medium > hard

---

## Performance Baseline

- Easy: ~0.71  
- Medium: ~0.64  
- Hard: ~0.53  

This demonstrates meaningful reward shaping and increasing task difficulty.

---

## Setup

```bash
pip install -r requirements.txt
uvicorn api.server:app --port 7860