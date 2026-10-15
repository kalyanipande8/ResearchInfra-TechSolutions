import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import pytest

from src.simulate_cluster_logs import simulate_uptime_log, simulate_job_queue, N_RESEARCHERS
from src.uptime_monitoring import compute_uptime
from src.capacity_optimization import compare_scheduling_policies, simulate_fifo, simulate_priority_aware


@pytest.fixture(scope="module")
def uptime_log():
    return simulate_uptime_log()


@pytest.fixture(scope="module")
def jobs():
    return simulate_job_queue()


def test_uptime_log_has_90_days_of_minutes(uptime_log):
    assert len(uptime_log) == 90 * 1440


def test_uptime_has_genuine_downtime_events(uptime_log):
    result = compute_uptime(uptime_log)
    assert result["n_downtime_events"] > 0
    assert result["uptime_pct"] < 100.0


def test_uptime_in_realistic_band(uptime_log):
    result = compute_uptime(uptime_log)
    assert 95.0 <= result["uptime_pct"] <= 100.0


def test_both_scheduling_policies_handle_all_jobs(jobs):
    fifo = simulate_fifo(jobs)
    priority = simulate_priority_aware(jobs)
    assert len(fifo) == len(jobs)
    assert len(priority) == len(jobs)


def test_priority_scheduling_reduces_high_priority_wait(jobs):
    result = compare_scheduling_policies(jobs)
    assert result["priority_high_priority_wait"] < result["fifo_high_priority_wait"]
