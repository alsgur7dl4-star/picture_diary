import time

import agents.image


def time_one_call(prompt: str, seed: int, model: str = "flux") -> float:
    t0 = time.perf_counter()
    agents.image.generate_image(prompt=prompt, seed=seed, model=model)
    t1 = time.perf_counter()
    return t1 - t0


def run_ab_test(prompt: str, n_calls: int = 1) -> dict:
    seed_a = 42
    seed_b = 137

    a_latencies: list[float] = []
    b_latencies: list[float] = []

    for i in range(n_calls):
        print(f"[A {i + 1}/{n_calls}] seed={seed_a} 호출")
        a_latencies.append(time_one_call(prompt, seed_a))
        print(f"[B {i + 1}/{n_calls}] seed={seed_b} 호출")
        b_latencies.append(time_one_call(prompt, seed_b))

    return {
        "seed_a": seed_a,
        "seed_b": seed_b,
        "a_latencies": a_latencies,
        "b_latencies": b_latencies,
        "n_calls": n_calls,
    }


def compute_p95(latencies: list[float]) -> float:
    if not latencies:
        return 0.0
    if len(latencies) <= 2:
        return max(latencies)

    sorted_latencies = sorted(latencies)
    n = len(sorted_latencies)
    rank = 0.95 * (n - 1)
    lower = int(rank)
    upper = min(lower + 1, n - 1)
    weight = rank - lower
    return sorted_latencies[lower] * (1 - weight) + sorted_latencies[upper] * weight
