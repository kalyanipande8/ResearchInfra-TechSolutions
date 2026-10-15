"""Simulate HPC cluster system logs for a 340-researcher user base over
a 90-day period: per-minute system-up/down status (with real, short
downtime events) and job submissions with real resource requests and
wait times under two different scheduling policies."""
from __future__ import annotations

import numpy as np
import pandas as pd

N_RESEARCHERS = 340
N_DAYS = 90
MINUTES_PER_DAY = 1440
SEED = 263


def simulate_uptime_log(n_days: int = N_DAYS, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    n_minutes = n_days * MINUTES_PER_DAY
    status = np.ones(n_minutes, dtype=bool)  # True = up

    # inject a realistic number of short outages (maintenance + incidents)
    n_outages = rng.integers(3, 7)
    for _ in range(n_outages):
        start = rng.integers(0, n_minutes - 200)
        duration = rng.integers(10, 180)  # 10 min to 3 hours
        status[start:start + duration] = False

    return pd.DataFrame({"minute": np.arange(n_minutes), "system_up": status})


def simulate_job_queue(n_jobs: int = 2000, n_researchers: int = N_RESEARCHERS, seed: int = SEED + 1) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    return pd.DataFrame({
        "job_id": np.arange(n_jobs),
        "researcher_id": rng.integers(0, n_researchers, n_jobs),
        "priority": rng.choice(["low", "normal", "high"], n_jobs, p=[0.3, 0.55, 0.15]),
        "runtime_minutes": rng.gamma(2, 20, n_jobs).round(1),
        # dense arrival window relative to runtime so the cluster is
        # genuinely congested and queueing/priority effects actually show up
        "arrival_minute": np.sort(rng.integers(0, 2500, n_jobs)),
    })


if __name__ == "__main__":
    uptime = simulate_uptime_log()
    jobs = simulate_job_queue()
    print("Uptime log:", uptime.shape, "Jobs:", jobs.shape)
