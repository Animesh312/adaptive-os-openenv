import random

class OSSimulator:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.seed = seed
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

        if action["action_type"] == "KILL":
            self.processes = [p for p in self.processes if p["pid"] != action["target_pid"]]

        elif action["action_type"] == "PRIORITIZE":
            for p in self.processes:
                if p["pid"] == action["target_pid"]:
                    p["priority"] = action["new_priority"]

        elif action["action_type"] == "SCHEDULE":
            self.processes.sort(key=lambda x: -x["priority"])

        # dynamic workload spike for hard task realism
        if self.timestep % 5 == 0:
            self.processes.append({
                "pid": len(self.processes),
                "cpu": self.rng.randint(20, 50),
                "memory": self.rng.randint(20, 50),
                "priority": self.rng.randint(1, 5)
            })

        # simulate CPU fluctuation
        for p in self.processes:
            p["cpu"] = max(1, p["cpu"] + self.rng.randint(-3, 5))

        return self._get_state()

    def _get_state(self):
        return {
            "cpu_usage": sum(p["cpu"] for p in self.processes),
            "memory_usage": sum(p["memory"] for p in self.processes),
            "processes": self.processes,
            "queue_length": len(self.processes),
            "timestep": self.timestep
        }