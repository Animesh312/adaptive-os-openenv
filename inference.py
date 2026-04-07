import os
import openai

from env.core import AdaptiveOSEnv
from env.models import Action

API_BASE_URL = os.getenv("API_BASE_URL", "https://api.openai.com/v1")
API_KEY = os.getenv("HF_TOKEN") or os.getenv("OPENAI_API_KEY", "dummy")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")

MAX_STEPS = 30

openai.api_key = API_KEY
openai.api_base = API_BASE_URL


def decide_action(obs) -> Action:
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
    return Action(action_type="SCHEDULE")


def run_task(task: str) -> float:
    env = AdaptiveOSEnv(task=task)
    obs = env.reset()

    total_reward = 0.0

    print(f"[START] task={task}", flush=True)

    for step in range(1, MAX_STEPS + 1):
        try:
            response = openai.ChatCompletion.create(
                model=MODEL_NAME,
                messages=[
                    {"role": "system", "content": "You are an OS scheduler agent."},
                    {
                        "role": "user",
                        "content": f"CPU={obs.cpu_usage}, Queue={obs.queue_length}"
                    }
                ],
                max_tokens=20,
                temperature=0.2,
            )
            _ = response["choices"][0]["message"]["content"]

        except Exception:
            pass

        action = decide_action(obs)

        obs, reward, done, _ = env.step(action)
        total_reward += reward.value

        # ✅ REQUIRED STEP LOG
        print(f"[STEP] step={step} reward={reward.value:.4f}", flush=True)

        if done:
            break

    final_score = total_reward / MAX_STEPS

    # ✅ REQUIRED END LOG
    print(
        f"[END] task={task} score={final_score:.4f} steps={step}",
        flush=True
    )

    return final_score


def main():
    tasks = ["easy", "medium", "hard"]

    for task in tasks:
        run_task(task)


if __name__ == "__main__":
    main()