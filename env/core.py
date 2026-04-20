import random

from env.simulator import OSSimulator
from env.models import Observation, Reward
from env.grader import compute_reward


class AdaptiveOSEnv:
    def __init__(self, task="easy", partial_observability=True, stochastic=True):
        self.task = task
        self.partial_observability = partial_observability
        self.stochastic = stochastic
        self.sim = OSSimulator()
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
        queue_length = state["queue_length"]

        # Improved reward function
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

        # Long-horizon: cumulative delay penalty
        self.cumulative_delay += queue_length
        long_horizon_penalty = -0.005 * self.cumulative_delay

        # Cost penalty
        cost_penalty = -state["cost"] * 0.01

        reward_val = cpu_reward + queue_reward + fairness_penalty + panic_bonus + long_horizon_penalty + cost_penalty

        reward_val = max(-1, min(1, reward_val))

        return (
            Observation(**state),
            Reward(value=reward_val),
            done_flag,
            info
        )

    def state(self):
        return Observation(**self.sim._get_state())