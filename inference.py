import os
import numpy as np
from stable_baselines3 import PPO
from stable_baselines3.common.env_util import make_vec_env
from env.gym_env import AdaptiveOSGymEnv
from env.core import AdaptiveOSEnv
from env.models import Action

MAX_STEPS = 30
MODEL_PATH = "ppo_adaptive_os.zip"

def train_rl_agent(task="easy", total_timesteps=10000):
    env = make_vec_env(lambda: AdaptiveOSGymEnv(task=task), n_envs=4)
    model = PPO("MlpPolicy", env, verbose=1, gamma=0.99, ent_coef=0.01, learning_rate=3e-4)
    model.learn(total_timesteps=total_timesteps)
    model.save(MODEL_PATH)
    return model

def load_rl_agent():
    if os.path.exists(MODEL_PATH):
        return PPO.load(MODEL_PATH)
    else:
        print("No trained model found, using heuristic")
        return None

def decide_action(obs) -> Action:
    model = load_rl_agent()
    if model:
        gym_env = AdaptiveOSGymEnv()
        gym_env.env.sim._get_state = lambda: obs.dict()  # hack to set state
        state = gym_env._get_state(obs)
        action_idx, _ = model.predict(state, deterministic=True)
        if action_idx == 0:
            return Action(action_type="SCHEDULE")
        elif action_idx == 1:
            heaviest = max(obs.processes, key=lambda p: p.cpu, default=None)
            return Action(action_type="KILL", target_pid=heaviest.pid if heaviest else 0)
        elif action_idx == 2:
            lowest = min(obs.processes, key=lambda p: p.priority, default=None)
            return Action(action_type="PRIORITIZE", target_pid=lowest.pid if lowest else 0, new_priority=5)
        else:
            return Action(action_type="SCHEDULE")
    else:
        # Improved heuristic
        if not obs.processes:
            return Action(action_type="SCHEDULE", target_pid=0)

        processes = obs.processes
        cpu_usage = obs.cpu_usage
        queue_length = obs.queue_length

        # sort helpers
        by_cpu = sorted(processes, key=lambda p: p.cpu, reverse=True)
        by_priority = sorted(processes, key=lambda p: p.priority)

        is_overloaded = cpu_usage > 85
        has_long_queue = queue_length > 6

        # 🔥 HANDLE GREEDY / PANIC (NEW INTELLIGENCE)
        greedy_procs = [p for p in processes if p.strategy == "greedy"]
        panic_procs = [p for p in processes if p.strategy == "panic"]

        # 1. overload → kill greedy first
        if is_overloaded:
            if greedy_procs:
                return Action(action_type="KILL", target_pid=greedy_procs[0].pid)
            return Action(action_type="KILL", target_pid=by_cpu[0].pid)

        # 2. panic near deadline → prioritize
        if panic_procs:
            return Action(action_type="PRIORITIZE", target_pid=panic_procs[0].pid, new_priority=5)

        # 3. long queue → prioritize efficient
        if has_long_queue:
            return Action(action_type="PRIORITIZE", target_pid=by_priority[0].pid, new_priority=5)

        # 4. default
        return Action(action_type="SCHEDULE", target_pid=by_cpu[0].pid)

def run_episode(task: str, policy_fn):
    env = AdaptiveOSEnv(task=task)
    obs = env.reset()

    total_cost = 0
    total_reward = 0
    rewards = []
    cpu_history = []
    queue_history = []

    for step in range(MAX_STEPS):
        action = policy_fn(obs)
        obs, reward, done, _ = env.step(action)

        total_cost += obs.cost
        total_reward += reward.value
        rewards.append(reward.value)
        cpu_history.append(obs.cpu_usage)
        queue_history.append(obs.queue_length)

        print(f"[STEP {step}] reward={reward.value:.3f} cpu={obs.cpu_usage} queue={obs.queue_length}")

        # strategy logging
        for p in obs.processes[:2]:
            print(f"   PID={p.pid} strat={p.strategy} cpu={p.cpu}")

        if done:
            break

    stability = max(queue_history) - min(queue_history)
    reward_variance = np.var(rewards)
    cpu_variance = np.var(cpu_history)
    queue_oscillation = sum(abs(queue_history[i] - queue_history[i-1]) for i in range(1, len(queue_history))) / len(queue_history)
    stability_score = 1 / (1 + stability + queue_oscillation)

    print("\n[METRICS]")
    print(f"Total Cost: {total_cost:.2f}")
    print(f"Avg Reward: {total_reward/MAX_STEPS:.3f}")
    print(f"Reward Variance: {reward_variance:.3f}")
    print(f"CPU Variance: {cpu_variance:.3f}")
    print(f"Queue Stability: {stability}")
    print(f"Queue Oscillation: {queue_oscillation:.3f}")
    print(f"Stability Score: {stability_score:.3f}")
    print(f"Peak Queue: {max(queue_history)}")
    print(f"Avg CPU: {sum(cpu_history)/len(cpu_history):.2f}")

    return total_cost


def main():
    # Train RL agent if not exists
    if not os.path.exists(MODEL_PATH):
        print("Training RL agent...")
        train_rl_agent(task="medium", total_timesteps=50000)  # train on medium
        print("Training complete.")

    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        print(f"\n===== TASK: {task.upper()} =====")

        print("\n--- RL AGENT ---")
        rl_cost = run_episode(task, decide_action)

        print("\n--- HEURISTIC ---")
        heuristic_cost = run_episode(task, heuristic_policy)

        improvement = ((heuristic_cost - rl_cost) / heuristic_cost) * 100 if heuristic_cost > 0 else 0

        print("\n===== COMPARISON =====")
        print(f"RL Cost: {rl_cost:.2f}")
        print(f"Heuristic Cost: {heuristic_cost:.2f}")
        print(f"Improvement: {improvement:.2f}%")
        print("======================\n")


if __name__ == "__main__":
    main()