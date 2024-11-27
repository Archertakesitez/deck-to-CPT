import csv

# Input and output file paths
input_file = "../data/cpt_codes.csv"
output_file = "../data/cpt_codes_cleaned.csv"

# Column name to filter
description_column = "Description"
filter_value = "No Summary found for this code"

# Read and filter the CSV file
with open(input_file, "r") as infile, open(output_file, "w", newline="") as outfile:
    reader = csv.DictReader(infile)
    # Write the filtered rows to the output file
    writer = csv.DictWriter(outfile, fieldnames=reader.fieldnames)
    writer.writeheader()

    for row in reader:
        if row[description_column] != filter_value:
            writer.writerow(row)

print(f"Filtered rows written to {output_file}")
