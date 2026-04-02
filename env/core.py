from env.simulator import OSSimulator
from env.models import Observation, Reward
from env.grader import compute_reward

class AdaptiveOSEnv:
    def __init__(self, task="easy"):
        self.sim = OSSimulator()
        self.task = task

    def reset(self):
        state = self.sim.reset()
        return Observation(**state)

    def step(self, action):
        state = self.sim.step(action.dict())
        reward_val, done = compute_reward(state, self.task)

        # penalty for overload
        if state["cpu_usage"] > 95:
            reward_val -= 0.2

        reward_val = max(0.0, min(1.0, reward_val))

        return (
            Observation(**state),
            Reward(value=reward_val),
            done,
            {}
        )

    def state(self):
        return Observation(**self.sim._get_state())