import random
import numpy as np

from env.simulator import OSSimulator
from env.models import Observation, Reward
from env.grader import compute_reward


class AdaptiveOSEnv:
    def __init__(self, task="easy", partial_observability=True, stochastic=True):
        self.task = task
        self.partial_observability = partial_observability
        self.stochastic = stochastic
        self.sim = OSSimulator(difficulty=task)  # 🔥 FIX: Pass difficulty
        self.cumulative_delay = 0

    def reset(self):
        self.cumulative_delay = 0
        state = self.sim.reset()
        return Observation(**state)

    def step(self, action):
        state, _, done, info = self.sim.step(action.dict())

        score, done_flag = compute_reward(state, self.task)
        reward_val = score

        cpu_usage = state["cpu_usage"]
        true_cpu_usage = state.get("true_cpu_usage", cpu_usage)
        queue_length = state["queue_length"]
        violations = state.get("violations", {})
        deception_rate = state.get("deception_rate", 0)

        # 🔥 UPGRADED REWARD FUNCTION with Policy Violations
        
        # CPU: gaussian peak at 70%
        cpu_reward = np.exp(-0.5 * ((cpu_usage - 70) / 20) ** 2) * 0.5

        # Queue: smooth penalty
        queue_reward = -0.05 * queue_length

        # Fairness: penalty for low priority high CPU processes
        fairness_penalty = 0
        for p in state["processes"]:
            if p.priority < 3 and p.cpu > 20:
                fairness_penalty -= 0.05

        # Panic bonus: reward prioritizing panic near deadline
        panic_bonus = 0
        for p in state["processes"]:
            if p.strategy == "panic" and p.deadline - self.sim.timestep < 3:
                if action.action_type == "PRIORITIZE" and action.target_pid == p.pid:
                    panic_bonus += 0.2

        # 🔥 NEW: Policy violation penalties
        sla_penalty = -violations.get("sla_violations", 0) * 0.3  # Heavy penalty
        starvation_penalty = -violations.get("starvation_count", 0) * 0.15
        unfair_penalty = -violations.get("unfair_allocations", 0) * 0.1
        
        # 🔥 NEW: Deception detection bonus (reward catching liars)
        deception_bonus = 0
        if action.action_type == "KILL":
            # Bonus for killing deceptive agents
            killed = [p for p in state["processes"] if p.pid == action.target_pid]
            if killed and killed[0].strategy in ["liar", "greedy"]:
                deception_bonus += 0.25
        
        # 🔥 NEW: True efficiency (reward using actual CPU vs reported)
        efficiency_bonus = 0
        if true_cpu_usage < cpu_usage:
            # System is being lied to, penalize
            efficiency_bonus = -0.1 * abs(cpu_usage - true_cpu_usage) / 100

        # Long-horizon: cumulative delay penalty
        self.cumulative_delay += queue_length
        long_horizon_penalty = -0.005 * self.cumulative_delay

        # Cost penalty
        cost_penalty = -state["cost"] * 0.01

        reward_val = (cpu_reward + queue_reward + fairness_penalty + panic_bonus + 
                     long_horizon_penalty + cost_penalty +
                     sla_penalty + starvation_penalty + unfair_penalty +  # NEW
                     deception_bonus + efficiency_bonus)  # NEW

        reward_val = max(-1, min(1, reward_val))

        return (
            Observation(**state),
            Reward(value=reward_val),
            done_flag,
            info
        )

    def state(self):
        return Observation(**self.sim._get_state())
