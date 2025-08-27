#
# python scripts/parse_vina_results.py <results_dir> <output_csv>
#
# Reads all Vina .log files in a directory, extracts the best binding
# affinity, and writes the results to a CSV file.
#

import os
import sys
import pandas as pd

def parse_vina_log(log_file):
    """Extracts the best binding affinity from a Vina log file."""
    best_affinity = None
    try:
        with open(log_file, 'r') as f:
            for line in f:
                # The best score is on a line that looks like:
                #   1      -9.5         0.000      0.000
                if line.strip().startswith('1 '):
                    parts = line.split()
                    best_affinity = float(parts[1])
                    break # Found the best score, no need to read further
    except Exception as e:
        print(f"Error reading {log_file}: {e}")
    return best_affinity

def main():
    if len(sys.argv) != 3:
        print("Usage: python parse_vina.py <results_directory> <output_csv_file>")
        sys.exit(1)

    results_dir = sys.argv[1]
    output_csv = sys.argv[2]

    results = []
    # Loop through all files in the results directory
    for filename in os.listdir(results_dir):
        if filename.endswith(".log"):
            log_path = os.path.join(results_dir, filename)
            affinity = parse_vina_log(log_path)
            if affinity is not None:
                # Get the CID from the filename
                cid = filename.replace(".log", "")
                results.append({'Ligand_CID': cid, 'Binding_Affinity_kcal_mol': affinity})

    if not results:
        print("No log files found or parsed in the directory.")
        return

    # Create a DataFrame and save to CSV
    df = pd.DataFrame(results)
    df = df.sort_values(by='Binding_Affinity_kcal_mol', ascending=True)
    df.to_csv(output_csv, index=False)
    print(f"Successfully created summary file: {output_csv}")

if __name__ == "__main__":
    main()