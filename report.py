# report.py
import os
import json
import csv

OUTPUT_DIR = os.path.join("data", "output")
REPORT_FILE = "data/report.csv"

HEADERS = [
    "puzzle_name", "size", "algorithm", "heuristic", "status",
    "solution_length", "time_taken", "space_used", "nodes_expanded"
]

def load_outputs():
    reports = []
    for filename in os.listdir(OUTPUT_DIR):
        if filename.endswith(".json"):
            filepath = os.path.join(OUTPUT_DIR, filename)
            with open(filepath, 'r') as f:
                data = json.load(f)
                report = {key: data.get(key, None) for key in HEADERS}
                reports.append(report)
    return reports

def write_csv(reports):
    os.makedirs(os.path.dirname(REPORT_FILE), exist_ok=True)
    with open(REPORT_FILE, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=HEADERS)
        writer.writeheader()
        writer.writerows(reports)
    print(f"Report written to {REPORT_FILE}")

def main():
    reports = load_outputs()
    if not reports:
        print("No output files found.")
        return
    write_csv(reports)

if __name__ == '__main__':
    main()
