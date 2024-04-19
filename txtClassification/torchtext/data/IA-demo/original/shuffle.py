import random

output_file = 'random.tsv'

with open(output_file, 'w') as outfile:
    with open('shuffled_lines.tsv', 'r') as infile:
        lines = infile.readlines()
        random.shuffle(lines)
        outfile.writelines(lines)


