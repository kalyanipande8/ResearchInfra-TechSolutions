"""End-to-end: simulate cluster uptime logs and job queue, compute real
uptime, and compare scheduling-policy performance."""
import json
import os

from src.simulate_cluster_logs import simulate_uptime_log, simulate_job_queue, N_RESEARCHERS
from src.uptime_monitoring import compute_uptime
from src.capacity_optimization import compare_scheduling_policies

os.makedirs("results", exist_ok=True)

print(f"=== Simulating 90-day cluster uptime log ({N_RESEARCHERS}-researcher user base) ===")
uptime_log = simulate_uptime_log()
uptime = compute_uptime(uptime_log)
print(uptime)

print("\n=== Simulating job queue and comparing scheduling policies ===")
jobs = simulate_job_queue()
scheduling = compare_scheduling_policies(jobs)
print(scheduling)

summary = {
    "n_researchers": N_RESEARCHERS,
    "uptime_pct": uptime["uptime_pct"],
    "n_downtime_events": uptime["n_downtime_events"],
    "fifo_high_priority_wait_min": scheduling["fifo_high_priority_wait"],
    "priority_high_priority_wait_min": scheduling["priority_high_priority_wait"],
    "high_priority_wait_reduction_pct": scheduling["high_priority_wait_reduction_pct"],
}
with open("results/summary.json", "w") as f:
    json.dump(summary, f, indent=2)

print("\n=== Summary ===")
print(json.dumps(summary, indent=2))
