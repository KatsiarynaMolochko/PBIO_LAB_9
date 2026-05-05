# Numer albumu: 30046
# Data: 05.05.2026
# Program generuje zapis FASTA dla pseudolosowej sekwencji DNA,
# z opcjonalnym wstawieniem imienia użytkownika w losowej pozycji.

import random


def generate_sequence(length: int) -> str:
    """ Returning random DNA sequence with nucleotides A, C, G, T."""
    nucleotides = ['A', 'C', 'G', 'T']
    return ''.join(random.choice(nucleotides) for _ in range(length))


def calculate_stats(sequence: str) -> dict:    
    """Calculates the percentage of each nucleotide and GC-content in the given DNA sequence."""
    total = len(sequence)
    if total == 0:
        return {"A": 0.0, "C": 0.0, "G": 0.0, "T": 0.0, "GC": 0.0}
    
    count_a = sequence.count('A')
    count_c = sequence.count('C')
    count_g = sequence.count('G')
    count_t = sequence.count('T')
    
    stats = {
        "A": round((count_a / total) * 100, 2),
        "C": round((count_c / total) * 100, 2),
        "G": round((count_g / total) * 100, 2),
        "T": round((count_t / total) * 100, 2),
        "GC": round(((count_g + count_c) / total) * 100, 2)
    }
    return stats


def insert_name(sequence: str, name: str) -> str:
    """Inserts the user's name at a random position in the sequence

    The name is written in lowercase letters to distinguish it visually
    in the FASTA file and not affect the nucleotide counting.
    """
    if not name:
        return sequence
    
    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]


def format_fasta(seq_id: str, description: str,
                sequence: str, line_width: int = 80) -> str:
    """creates a valid FASTA record with a header and line breaks."""
    if description:
        header = f">{seq_id} {description}"
    else:
        header = f">{seq_id}"
    
    formatted_seq = ""
    for i in range(0, len(sequence), line_width):
        formatted_seq += sequence[i:i+line_width] + "\n"
    
    return header + "\n" + formatted_seq


def validate_positive_int(input_str: str,
                         min_val: int = 1,
                         max_val: int = 100_000) -> int:
    """Returns a positive integer from user input and validates the range"""
    while True:
        try:
            value = int(input(input_str))
            if min_val <= value <= max_val:
                return value
            else:
                print(f"Error: value must be between [{min_val}, {max_val}].")
        except ValueError:
            print("Error: Please enter a valid integer.")


def main():
    length = validate_positive_int("Enter the length of the DNA sequence (1-100000): ")
    
    while True:
        seq_id = input("Enter the sequence ID (no whitespace allowed): ").strip()
        if seq_id and ' ' not in seq_id and '\t' not in seq_id:
            break
        print("Error: ID cannot contain whitespace.")
    
    
    description = input("Enter the sequence description (optional): ").strip()
    name = input("Enter your name: ").strip()
    

    sequence = generate_sequence(length)
    sequence_with_name = insert_name(sequence, name)
    stats = calculate_stats(sequence)
    fasta_content = format_fasta(seq_id, description, sequence_with_name)
    
   
    filename = f"{seq_id}.fasta"
    with open(filename, 'w') as f:
        f.write(fasta_content)
    
    print(f"\nSequence saved to file: {filename}")
    print("\nSequence statistics:")
    print(f"A: {stats['A']} %")
    print(f"C: {stats['C']} %")
    print(f"G: {stats['G']} %")
    print(f"T: {stats['T']} %")
    print(f"GC-content: {stats['GC']} %")


if __name__ == "__main__":
    main()