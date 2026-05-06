# Numer albumu: 30046
# Data: 05.05.2026
# Program generuje zapis FASTA dla pseudolosowej sekwencji DNA,
# z opcjonalnym wstawieniem imienia użytkownika w losowej pozycji.
# Dodatkowo, program oblicza i wyświetla statystyki procentowe dla każdego nukleotydu oraz zawartości GC.  

# tryby działania: 
# pojedynczy rekord FASTA
# generowanie wielu rekordów FASTA w jednym pliku
# rekordy dla sekwencji komplementarnej i odwrotnie-komplementarnej


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


def complement_sequence(sequence: str) -> str:
    """Returns the complementary DNA strand (5'->3', same direction as input)."""
    complement_map = str.maketrans('ACGTacgt', 'TGCAtgca')
    return sequence.translate(complement_map)


def reverse_complement_sequence(sequence: str) -> str:
    """Returns the reverse complementary strand (antiparallel complement, 3'->5' read as 5'->3')."""
    return complement_sequence(sequence)[::-1]


def generate_single_fasta(length: int,
                          seq_id: str,
                          description: str,
                          name: str,
                          output_filename: str) -> None:
    """Generate a single FASTA record and write it to a file."""
    sequence = generate_sequence(length)
    sequence_with_name = insert_name(sequence, name)
    fasta_content = format_fasta(seq_id, description, sequence_with_name)

    with open(output_filename, 'w') as f:
        f.write(fasta_content)

    stats = calculate_stats(sequence)
    print(f"\nSequence saved to file: {output_filename}")
    print("\nSequence statistics:")
    print(f"A: {stats['A']} %")
    print(f"C: {stats['C']} %")
    print(f"G: {stats['G']} %")
    print(f"T: {stats['T']} %")
    print(f"GC-content: {stats['GC']} %")


def generate_complement_fasta(length: int,
                              seq_id: str,
                              description: str, 
                              output_filename: str) -> None:
    """Generate original, complementary, and reverse complementary FASTA records in one file."""
    sequence = generate_sequence(length)
    
    comp_seq = complement_sequence(sequence)
    rev_comp_seq = reverse_complement_sequence(sequence)

    fasta_content = format_fasta(seq_id, description, sequence)
    fasta_content += format_fasta(f"{seq_id}_complement", description, comp_seq)
    fasta_content += format_fasta(f"{seq_id}_revcomp", description, rev_comp_seq)

    with open(output_filename, 'w') as f:
        f.write(fasta_content)

    stats = calculate_stats(sequence)
    print(f"\nThree records saved to file: {output_filename}")
    print(f"  Records: {seq_id}, {seq_id}_complement, {seq_id}_revcomp")
    print("\nOriginal sequence statistics:")
    print(f"A: {stats['A']} %")
    print(f"C: {stats['C']} %")
    print(f"G: {stats['G']} %")
    print(f"T: {stats['T']} %")
    print(f"GC-content: {stats['GC']} %")


def generate_batch_fasta(batch_count: int,
                         length: int,
                         description: str,
                         output_filename: str) -> None:
    """Generate multiple FASTA records in a single multi-FASTA file."""
    fasta_records = ""
    digit_width = len(str(batch_count))

    for index in range(1, batch_count + 1):
        seq_id = f"Seq_{index:0{digit_width}d}"
        sequence = generate_sequence(length)
        fasta_records += format_fasta(seq_id, description, sequence)

        stats = calculate_stats(sequence)
        print(
            f"{seq_id}: A={stats['A']}%, C={stats['C']}%, G={stats['G']}%, "
            f"T={stats['T']}%, GC={stats['GC']}%")

    with open(output_filename, 'w') as f:
        f.write(fasta_records)


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


def choose_mode() -> str:
    """Ask the user to choose between single, batch, or complement generation mode."""
    while True:
        choice = input(
            "Choose mode: [1] single sequence, [2] batch multi-FASTA, "
            "[3] complement (original + complement + reverse complement): "
        ).strip()
        if choice == '1' or choice.lower() in ('single', 's'):
            return 'single'
        if choice == '2' or choice.lower() in ('batch', 'b'):
            return 'batch'
        if choice == '3' or choice.lower() in ('complement', 'c'):
            return 'complement'
        print("Error: choose 1 for single, 2 for batch, or 3 for complement mode.")



def main():
    mode = choose_mode()


    match mode:
        case 'single':
            length = validate_positive_int(
                "Input sequence length in range (1-100000): ")

            while True:
                seq_id = input("Input sequence ID (no whitespace): ").strip()
                if seq_id and ' ' not in seq_id and '\t' not in seq_id:
                    break
                print("Error: ID cannot contain whitespace.")

            description = input("Input sequence description (optional): ").strip()
            name = input("Input your name: ").strip()

            output_file = input(
                "Input output file name (without extension, default 'sequence'): "
            ).strip()
            if not output_file:
                output_file = "sequence"
            output_filename = f"{output_file.replace(' ', '_')}.fasta"

            generate_single_fasta(length, seq_id, description, name, output_filename)

        case 'batch':
            batch_count = validate_positive_int(
                "Input number of sequences to generate: ", min_val=1, max_val=1000)
            length = validate_positive_int(
                "Input sequence length in range (1-100000): ")
            description = input("Input sequence description (optional): ").strip()

            output_file = input(
                "Input output file name (without extension, default 'multi_sequences'): "
            ).strip()
            if not output_file:
                output_file = "multi_sequences"
            output_filename = f"{output_file.replace(' ', '_')}.fasta"

            generate_batch_fasta(batch_count, length, description, output_filename)
            print(f"\nGenerated {batch_count} sequences and saved them to file: {output_filename}")

        case 'complement':
            length = validate_positive_int(
                "Input sequence length in range (1-100000): ")

            while True:
                seq_id = input("Input sequence ID (no whitespace): ").strip()
                if seq_id and ' ' not in seq_id and '\t' not in seq_id:
                    break
                print("Error: ID cannot contain whitespace.")

            description = input("Input sequence description (optional): ").strip()

            output_file = input(
                "Input output file name (without extension, default 'complement'): "
            ).strip()
            if not output_file:
                output_file = "complement"
            output_filename = f"{output_file.replace(' ', '_')}.fasta"

            generate_complement_fasta(length, seq_id, description, output_filename)


if __name__ == "__main__":
    main()