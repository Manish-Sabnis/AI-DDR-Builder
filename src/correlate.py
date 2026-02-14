def correlate_data(inspection_data, thermal_data):
    if not thermal_data:
        avg_coldspot = None
    else:
        avg_coldspot = sum(t["coldspot"] for t in thermal_data) / len(thermal_data)

    correlated = []

    for item in inspection_data:
        severity = "Moderate"

        if avg_coldspot and avg_coldspot < 21.5:
            severity = "High"

        correlated.append({
            "location": item["location"],
            "issue": item["issue"],
            "average_coldspot": round(avg_coldspot, 2) if avg_coldspot else "Not Available",
            "severity": severity
        })

    return correlated
