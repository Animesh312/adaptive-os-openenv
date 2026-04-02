from pydantic import BaseModel
from typing import List, Optional

class Process(BaseModel):
    pid: int
    cpu: float
    memory: float
    priority: int

class Observation(BaseModel):
    cpu_usage: float
    memory_usage: float
    processes: List[Process]
    queue_length: int
    timestep: int

class Action(BaseModel):
    action_type: str  # SCHEDULE | KILL | PRIORITIZE
    target_pid: Optional[int] = None
    new_priority: Optional[int] = None

class Reward(BaseModel):
    value: float