import os
from extract import extract_inspection_data, extract_thermal_data
from correlate import correlate_data
from generate import generate_ddr


def main():
    inspection_path = "data/Sample Report.pdf"
    thermal_path = "data/Thermal Images.pdf"

    inspection_data = extract_inspection_data(inspection_path)
    thermal_data = extract_thermal_data(thermal_path)

    print("Inspection Data:", inspection_data)
    print("Thermal Data:", thermal_data)


    correlated = correlate_data(inspection_data, thermal_data)

    report = generate_ddr(correlated)

    

    os.makedirs("outputs", exist_ok=True)

    with open("outputs/DDR_Report.md", "w") as f:
        f.write(report)

    print("DDR report generated in outputs/DDR_Report.md")


if __name__ == "__main__":
    main()
