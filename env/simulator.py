import random
from env.models import Process

class OSSimulator:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        self.timestep = 0
        self.processes = [
            {
                "pid": i,
                "cpu": self.rng.randint(5, 30),
                "memory": self.rng.randint(10, 40),
                "priority": self.rng.randint(1, 5),
            }
            for i in range(5)
        ]
        return self._get_state()


    def step(self, action):
        self.timestep += 1  

        # 🔥 Apply action
        if action["action_type"] == "KILL":
            self.processes = [p for p in self.processes if p["pid"] != action["target_pid"]]

        elif action["action_type"] == "PRIORITIZE":
            for p in self.processes:
                if p["pid"] == action["target_pid"]:
                    p["priority"] = action["new_priority"]

        elif action["action_type"] == "SCHEDULE":
            self.processes.sort(key=lambda x: -x["priority"])

        # 🔥 Dynamic workload spike
        if self.timestep % 5 == 0:
            self.processes.append({
                "pid": len(self.processes),
                "cpu": self.rng.randint(20, 50),
                "memory": self.rng.randint(20, 50),
                "priority": self.rng.randint(1, 5)
            })

        # 🔥 Random burst load (better than broken queue logic)
        if self.rng.random() < 0.2:
            self.processes.append({
                "pid": len(self.processes),
                "cpu": self.rng.randint(10, 30),
                "memory": self.rng.randint(10, 30),
                "priority": self.rng.randint(1, 5)
            })

        # 🔥 Prevent explosion
        if len(self.processes) > 10:
            self.processes.pop(0)

        # 🔥 CPU fluctuation
        for p in self.processes:
            p["cpu"] = max(1, p["cpu"] + self.rng.randint(-3, 5))

        return self._get_state(), None, self.timestep >= 30, {}


    def _get_state(self):
        cpu_usage = min(100, sum(p["cpu"] for p in self.processes))
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": sum(p["memory"] for p in self.processes),
            "processes": [Process(**p) for p in self.processes],
            "queue_length": len(self.processes),
            "timestep": self.timestep,
            "cost": cpu_usage * 0.05
        }
    