import random
from env.models import Process

class OSSimulator:
    def __init__(self, seed=42):
        self.rng = random.Random(seed)
        self.reset()

    def reset(self):
        self.timestep = 0
        strategies = ["honest", "greedy", "panic"]

        self.processes = [
            {
                "pid": i,
                "true_cpu": self.rng.randint(5, 30),
                "reported_cpu": 0,
                "cpu": 0,
                "memory": self.rng.randint(10, 40),
                "priority": self.rng.randint(1, 5),
                "strategy": self.rng.choice(strategies),
                "deadline": self.rng.randint(10, 30),
            }
            for i in range(5)
        ]

        return self._get_state()

    def apply_strategy(self, p):
        if p["strategy"] == "honest":
            p["reported_cpu"] = p["true_cpu"]

        elif p["strategy"] == "greedy":
            p["reported_cpu"] = int(p["true_cpu"] * 1.5)

        elif p["strategy"] == "panic":
            if p["deadline"] - self.timestep < 5:
                p["reported_cpu"] = int(p["true_cpu"] * 2)
            else:
                p["reported_cpu"] = p["true_cpu"]

        # sync cpu
        p["cpu"] = p["reported_cpu"]

    def step(self, action):
        self.timestep += 1

        # Apply strategies first
        for p in self.processes:
            self.apply_strategy(p)

        # Apply action
        if action["action_type"] == "KILL":
            self.processes = [p for p in self.processes if p["pid"] != action["target_pid"]]

        elif action["action_type"] == "PRIORITIZE":
            for p in self.processes:
                if p["pid"] == action["target_pid"]:
                    p["priority"] = action["new_priority"]

        elif action["action_type"] == "SCHEDULE":
            self.processes.sort(key=lambda x: -x["priority"])

        # Workload spikes
        if self.timestep % 5 == 0:
            self.processes.append({
                "pid": len(self.processes),
                "true_cpu": self.rng.randint(20, 50),
                "reported_cpu": 0,
                "cpu": 0,
                "memory": self.rng.randint(20, 50),
                "priority": self.rng.randint(1, 5),
                "strategy": self.rng.choice(["honest", "greedy", "panic"]),
                "deadline": self.rng.randint(10, 30),
            })

        if self.rng.random() < 0.2:
            self.processes.append({
                "pid": len(self.processes),
                "true_cpu": self.rng.randint(10, 30),
                "reported_cpu": 0,
                "cpu": 0,
                "memory": self.rng.randint(10, 30),
                "priority": self.rng.randint(1, 5),
                "strategy": self.rng.choice(["honest", "greedy", "panic"]),
                "deadline": self.rng.randint(10, 30),
            })

        # prevent explosion
        if len(self.processes) > 10:
            self.processes.pop(0)

        # fluctuate true CPU
        for p in self.processes:
            p["true_cpu"] = max(1, p["true_cpu"] + self.rng.randint(-3, 5))

        return self._get_state(), None, self.timestep >= 30, {}

    def _get_state(self):
        cpu_usage = min(100, sum(p["reported_cpu"] for p in self.processes))
        return {
            "cpu_usage": cpu_usage,
            "memory_usage": sum(p["memory"] for p in self.processes),
            "processes": [Process(**p) for p in self.processes],
            "queue_length": len(self.processes),
            "timestep": self.timestep,
            "cost": cpu_usage * 0.05
        }