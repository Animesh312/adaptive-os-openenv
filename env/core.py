import random
import numpy as np

from env.simulator import OSSimulator
from env.models import Observation, Reward
from env.grader import compute_reward

class AdaptiveOSEnv:
    def __init__(self, partial_observability=True, stochastic=True):
        self.partial_observability = partial_observability
        self.stochastic = stochastic

    def _get_full_state(self):
        return {
            "cpu": self.cpu_usage,
            "queue": self.queue_length,
            "processes": self.processes,
            "timestep": self.timestep
        }
    
    def _get_observation(self):
        if not self.partial_observability:
            return self._get_full_state()

        return {
            "cpu_estimate": round(self.cpu_usage + np.random.normal(0, 5), 2),
            "queue_estimate": self.queue_length,
            "visible_processes": random.sample(
                self.processes,
                k=min(3, len(self.processes))
            ),
            "timestep": self.timestep
        }

    def reset(self):
        state = self.sim.reset()
        return Observation(**state)

    def step(self, action):
        state, _, done, info = self.sim.step(action.dict())

        # ✅ reward from grader
        score, done_flag = compute_reward(state, self.task)

        # 🔥 OPTIMIZED REWARD SHAPING (FOCUSED ON KEY METRICS)
        reward_val = score

        cpu_usage = state["cpu_usage"]
        queue_length = state["queue_length"]

        # CPU stability (sweet spot: 60-80%)
        if 60 <= cpu_usage <= 80:
            reward_val += 0.15  # Bonus for optimal utilization
        elif cpu_usage > 90:
            reward_val -= 0.4  # Heavy penalty for overload
        elif cpu_usage < 40:
            reward_val -= 0.2  # Penalty for underutilization

        # Queue efficiency
        if queue_length <= 4:
            reward_val += 0.1  # Bonus for manageable queues
        elif queue_length > 7:
            reward_val -= 0.25  # Penalty for long queues

        # Action appropriateness
        if action.action_type == "KILL":
            # Reward killing only when necessary
            if cpu_usage > 85:
                reward_val += 0.1
            else:
                reward_val -= 0.15  # Penalty for unnecessary killing

        elif action.action_type == "PRIORITIZE":
            # Reward prioritization for queue management
            if queue_length > 5:
                reward_val += 0.12
            elif cpu_usage > 75:
                reward_val += 0.08

        # Cost efficiency (small penalty for high costs)
        reward_val -= state["cost"] * 0.002

        # Clamp to reasonable range
        reward_val = max(-0.5, min(1.5, reward_val))

        return (
            Observation(**state),
            Reward(value=reward_val),
            done_flag,
            info
        )

    def state(self):
        return Observation(**self.sim._get_state())