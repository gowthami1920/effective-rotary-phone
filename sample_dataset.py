input_file = r"C:\Users\nalla\Downloads\soc-pokec-relationships.txt\soc-pokec-relationships.txt"
output_file = "pokec_sample.txt"

count = 0
limit = 5000

with open(input_file, "r") as infile, open(output_file, "w") as outfile:
    # Header
    outfile.write("source\ttarget\n")

    for line in infile:
        if line.startswith("#"):
            continue

        outfile.write(line)
        count += 1

        if count >= limit:
            break

print(f"Done! Created {output_file} with {count} relationships.")