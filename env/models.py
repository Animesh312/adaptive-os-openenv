from pydantic import BaseModel
from typing import List, Optional

class Process(BaseModel):
    pid: int
    cpu: float
    memory: float
    priority: int

    # Safe defaults (critical fix)
    true_cpu: float = 0
    reported_cpu: float = 0
    strategy: str = "honest"
    deadline: int = 0


class Observation(BaseModel):
    cpu_usage: float
    memory_usage: float
    processes: List[Process]
    queue_length: int
    timestep: int
    cost: float = 0.0


class Action(BaseModel):
    action_type: str  # SCHEDULE | KILL | PRIORITIZE
    target_pid: Optional[int] = None
    new_priority: Optional[int] = None


class Reward(BaseModel):
    value: float