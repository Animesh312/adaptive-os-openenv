from fastapi import FastAPI
from env.core import AdaptiveOSEnv
from env.models import Action

app = FastAPI()
env = AdaptiveOSEnv()

@app.post("/reset")
def reset():
    return env.reset().dict()

@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
    return {
        "observation": obs.dict(),
        "reward": reward.value,
        "done": done,
        "info": info
    }

@app.get("/state")
def state():
    return env.state().dict()