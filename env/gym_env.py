import gymnasium as gym
import numpy as np
from env.core import AdaptiveOSEnv
from env.models import Action

class AdaptiveOSGymEnv(gym.Env):
    def __init__(self, task="easy"):
        super().__init__()
        self.env = AdaptiveOSEnv(task=task)
        self.prev_queue = 0
        self.prev_cpu = 0
        self.reward_history = []

        # Action space: 0=SCHEDULE, 1=KILL, 2=PRIORITIZE, 3=DO_NOTHING
        self.action_space = gym.spaces.Discrete(4)

        # 🔥 UPGRADED State space: flattened features
        # cpu_norm, queue_delta, load_level, reward_trend, process_features (flattened)
        # process_features: for each process: strategy_onehot (5), cpu_demand_norm, waiting_time_norm, deception_signal
        max_procs = 10
        proc_features = 5 + 1 + 1 + 1  # strategy(5) + cpu + waiting + deception
        state_dim = 1 + 1 + 1 + 1 + max_procs * proc_features  # cpu, queue_delta, load, reward_trend, procs
        self.observation_space = gym.spaces.Box(low=-np.inf, high=np.inf, shape=(state_dim,), dtype=np.float32)

    def reset(self, seed=None, options=None):
        if seed is not None:
            np.random.seed(seed)
        obs = self.env.reset()
        self.prev_queue = obs.queue_length
        self.prev_cpu = obs.cpu_usage
        self.reward_history = []
        return self._get_state(obs), {}

    def step(self, action):
        # Map action to Action model
        if action == 0:
            act = Action(action_type="SCHEDULE")
        elif action == 1:
            heaviest = max(self.env.state().processes, key=lambda p: p.cpu, default=None)
            act = Action(action_type="KILL", target_pid=heaviest.pid if heaviest else 0)
        elif action == 2:
            lowest = min(self.env.state().processes, key=lambda p: p.priority, default=None)
            act = Action(action_type="PRIORITIZE", target_pid=lowest.pid if lowest else 0, new_priority=5)
        else:  # 3
            act = Action(action_type="SCHEDULE")  # do nothing equivalent

        obs, reward, done, info = self.env.step(act)
        state = self._get_state(obs)
        self.reward_history.append(reward.value)
        # Gymnasium expects 5 values: (obs, reward, terminated, truncated, info)
        return state, reward.value, done, False, info

    def _get_state(self, obs):
        cpu_norm = obs.cpu_usage / 100.0
        queue_delta = obs.queue_length - self.prev_queue
        self.prev_queue = obs.queue_length

        load_level = 0 if obs.cpu_usage < 40 else 1 if obs.cpu_usage < 80 else 2  # low, med, high

        reward_trend = np.mean(self.reward_history[-5:]) if self.reward_history else 0

        proc_features = []
        # 🔥 UPGRADED: Handle all agent strategies
        all_strategies = ["honest", "greedy", "panic", "liar", "adversarial"]
        
        for p in obs.processes[:10]:  # max 10
            # One-hot encode strategy (5 strategies now)
            strategy_onehot = [1 if p.strategy == s else 0 for s in all_strategies]
            cpu_demand_norm = p.true_cpu / 50.0  # assume max 50
            waiting_time_norm = p.wait_time / 15.0  # normalize wait time
            
            # 🔥 NEW: Add deception signal (reported vs true)
            deception_signal = (p.reported_cpu - p.true_cpu) / max(p.true_cpu, 1.0)
            
            proc_features.extend(strategy_onehot + [cpu_demand_norm, waiting_time_norm, deception_signal])

        # Pad to max_procs (now 8 features per process: 5 strategy + cpu + wait + deception)
        while len(proc_features) < 10 * 8:
            proc_features.extend([0] * 8)

        state = [cpu_norm, queue_delta, load_level, reward_trend] + proc_features
        return np.array(state, dtype=np.float32)

    def render(self, mode='human'):
        pass
