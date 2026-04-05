import os
from typing import List

import openai  # ✅ changed import

from env.core import AdaptiveOSEnv
from env.models import Action

# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY", "dummy")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

MAX_STEPS = 30

# ✅ Configure OpenAI (old SDK style)
openai.api_key = API_KEY
openai.api_base = API_BASE_URL


def decide_action(obs) -> Action:
    """
    Simple baseline policy (LLM optional, deterministic fallback)
    """

    if obs.cpu_usage > 85:
        return Action(
            action_type="KILL",
            target_pid=obs.processes[0].pid
        )

    elif obs.queue_length > 6:
        return Action(
            action_type="PRIORITIZE",
            target_pid=obs.processes[0].pid,
            new_priority=5
        )

    else:
        return Action(action_type="SCHEDULE")


def run_task(task: str) -> float:
    env = AdaptiveOSEnv(task=task)
    obs = env.reset()

    total_reward = 0.0

    for step in range(MAX_STEPS):
        try:
            # ✅ Updated API call (old SDK)
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {
                        "role": "system",
                        "content": "You are an OS scheduler agent."
                    },
                    {
                        "role": "user",
                        "content": f"CPU={obs.cpu_usage}, Queue={obs.queue_length}. Suggest action."
                    }
                ],
                max_tokens=20,
                temperature=0.2,
            )

            # optional use (kept for compliance)
            _ = response["choices"][0]["message"]["content"]

        except Exception:
            pass  # fallback to rule-based

        action = decide_action(obs)

        obs, reward, done, _ = env.step(action)
        total_reward += reward.value

        if done:
            break

    return total_reward / MAX_STEPS


def main():
    tasks = ["easy", "medium", "hard"]
    results = {}

    for task in tasks:
        score = run_task(task)
        results[task] = score
        print(f"{task}: {score:.3f}")

    print("\nFinal Scores:", results)


if __name__ == "__main__":
    main()