def correlate_data(inspection_data, thermal_data):
    if not thermal_data:
        avg_coldspot = None
        min_coldspot = None
    else:
        avg_coldspot = sum(t["coldspot"] for t in thermal_data) / len(thermal_data)
        min_coldspot = min(t["coldspot"] for t in thermal_data)

    correlated = {
        "inspection_findings": inspection_data,
        "thermal_summary": {
            "average_coldspot": round(avg_coldspot, 2) if avg_coldspot else "Not Available",
            "minimum_coldspot": min_coldspot if min_coldspot else "Not Available",
            "total_thermal_images_processed": len(thermal_data)
        }
    }

    return correlated

