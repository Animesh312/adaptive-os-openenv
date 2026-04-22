from fastapi import FastAPI
from env.core import AdaptiveOSEnv
from env.models import Action
from inference import decide_action, load_rl_agent

app = FastAPI()
env = AdaptiveOSEnv()


@app.on_event("startup")
async def startup_event():
    """🔥 Preload model at server startup to avoid first-call latency"""
    print("\n🚀 Starting API server...")
    print("📦 Preloading RL model...")
    load_rl_agent()  # This will cache the model globally
    print("✅ Server ready!\n")


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
