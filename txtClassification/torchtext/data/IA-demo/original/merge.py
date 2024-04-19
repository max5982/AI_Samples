import random

def shuffle_lines(input_files, output_file):
    with open(output_file, 'w') as outfile:
        for input_file in input_files:
            with open(input_file, 'r') as infile:
                lines = infile.readlines()
                random.shuffle(lines)
                outfile.writelines(lines)

# Example usage
input_files = ['control.tsv', 'general.tsv', 'rag.tsv']
output_file = 'shuffled_lines.tsv'
shuffle_lines(input_files, output_file)
