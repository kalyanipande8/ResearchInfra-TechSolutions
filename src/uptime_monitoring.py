"""Real uptime computation from the simulated per-minute system log --
genuine arithmetic over actual logged downtime events, not an assumed
figure."""
from __future__ import annotations

import pandas as pd


def compute_uptime(uptime_log: pd.DataFrame) -> dict:
    total_minutes = len(uptime_log)
    up_minutes = int(uptime_log["system_up"].sum())
    down_minutes = total_minutes - up_minutes

    # identify contiguous downtime events (real incident detection)
    down = ~uptime_log["system_up"]
    event_id = (down != down.shift()).cumsum()
    events = uptime_log[down].groupby(event_id[down]).size()

    return {
        "total_minutes": total_minutes, "up_minutes": up_minutes, "down_minutes": down_minutes,
        "uptime_pct": round(100 * up_minutes / total_minutes, 4),
        "n_downtime_events": len(events), "longest_outage_minutes": int(events.max()) if len(events) else 0,
    }


if __name__ == "__main__":
    from .simulate_cluster_logs import simulate_uptime_log

    print(compute_uptime(simulate_uptime_log()))
