def compute_reward(state, task):
    cpu = state["cpu_usage"]
    queue = state["queue_length"]

    if task == "easy":
        score = max(0.0, min(1.0, (100 - cpu) / 100))

    elif task == "medium":
        score = max(0.0, min(1.0, 1 / (1 + queue)))

    else:  # hard
        stability = max(0.0, (100 - cpu) / 100)
        throughput = max(0.0, 1 / (1 + queue))
        score = 0.5 * stability + 0.5 * throughput

    done = state["timestep"] >= 30

    return score, done