from fastapi import FastAPI
from env.core import AdaptiveOSEnv
from env.models import Action
from inference import decide_action

app = FastAPI()
env = AdaptiveOSEnv()


@app.post("/reset")
def reset():
    return env.reset()   # no .dict()

@app.post("/step")
def step():
    obs = env.state()  # ✅ already Observation

    action = decide_action(obs)

    new_obs, reward, done, _ = env.step(action)

    return {
        "cpu": new_obs.cpu_usage,
        "queue": new_obs.queue_length,
        "cost": new_obs.cost,
        "action": action.action_type,
        "target": action.target_pid
    }

@app.get("/state")
def state():
    return env.sim._get_state()