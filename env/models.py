from pydantic import BaseModel
from typing import List, Optional, Dict

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
    wait_time: int = 0  # NEW: Track starvation
    requested_cpu: float = 0  # NEW: What agent requests
    is_critical: bool = False  # NEW: SLA-critical process


class Observation(BaseModel):
    cpu_usage: float
    memory_usage: float
    processes: List[Process]
    queue_length: int
    timestep: int
    cost: float = 0.0
    
    # 🔥 NEW FIELDS for multi-agent intelligence
    true_cpu_usage: float = 0.0  # Actual CPU need vs reported
    violations: Dict[str, int] = {}  # Policy violations
    deception_rate: float = 0.0  # How much agents lie
    agent_requests: List[Dict] = []  # Agent negotiation history


class Action(BaseModel):
    action_type: str  # SCHEDULE | KILL | PRIORITIZE
    target_pid: Optional[int] = None
    new_priority: Optional[int] = None


class Reward(BaseModel):
    value: float
