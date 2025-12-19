import pandas as pd
import numpy as np

def simulate_driver_allocation(
    total_drivers: int = 300
):
    """
    Simulates driver allocation based on demand zones
    """

    # Load clustered data
    data = pd.read_csv("data/ride_data_with_zones.csv")

    # Aggregate demand per zone
    zone_summary = data.groupby("zone_cluster")["ride_demand"].sum().reset_index()

    total_demand = zone_summary["ride_demand"].sum()

    # Naive allocation (equal drivers per zone)
    naive_drivers = total_drivers / len(zone_summary)

    # Demand-aware allocation
    zone_summary["allocated_drivers"] = (
        zone_summary["ride_demand"] / total_demand
    ) * total_drivers

    # Waiting time simulation
    # Waiting time ∝ demand / drivers
    zone_summary["naive_wait_time"] = (
        zone_summary["ride_demand"] / naive_drivers
    )

    zone_summary["optimized_wait_time"] = (
        zone_summary["ride_demand"] / zone_summary["allocated_drivers"]
    )

    # Calculate reduction %
    zone_summary["waiting_time_reduction_%"] = (
        (zone_summary["naive_wait_time"] - zone_summary["optimized_wait_time"])
        / zone_summary["naive_wait_time"]
    ) * 100

    avg_reduction = zone_summary["waiting_time_reduction_%"].mean()

    result = {
        "total_drivers": total_drivers,
        "average_waiting_time_reduction_percent": round(avg_reduction, 2),
        "zone_level_summary": zone_summary.to_dict(orient="records")
    }

    return result
