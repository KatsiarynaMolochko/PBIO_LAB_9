# Numer albumu: 30046
# Data: 05.05.2026
# Program generuje zapis FASTA dla pseudolosowej sekwencji DNA,
# z opcjonalnym wstawieniem imienia użytkownika w losowej pozycji.
# Dodatkowo, program oblicza i wyświetla statystyki procentowe dla każdego nukleotydu oraz zawartości GC.

# tryby działania:
# pojedynczy rekord FASTA
# generowanie wielu rekordów FASTA w jednym pliku
# rekordy dla sekwencji komplementarnej i odwrotnie-komplementarnej
# transkrypcja sekwencji DNA do mRNA (zamiana T na U)
# wyszukiwanie motywów w sekwencji DNA


import random


def generate_sequence(length: int) -> str:
    """Returning random DNA sequence with nucleotides A, C, G, T."""
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

    return {
        "A": round((count_a / total) * 100, 2),
        "C": round((count_c / total) * 100, 2),
        "G": round((count_g / total) * 100, 2),
        "T": round((count_t / total) * 100, 2),
        "GC": round(((count_g + count_c) / total) * 100, 2),
    }


def insert_name(sequence: str, name: str) -> str:
    """Inserts the user's name at a random position in the sequence.

    The name is written in lowercase letters to distinguish it visually
    in the FASTA file and not affect the nucleotide counting.
    """
    if not name:
        return sequence
    position = random.randint(0, len(sequence))
    return sequence[:position] + name.lower() + sequence[position:]


def format_fasta(seq_id: str, description: str,
                 sequence: str, line_width: int = 80) -> str:
    """Creates a valid FASTA record with a header and line breaks."""
    header = f">{seq_id} {description}" if description else f">{seq_id}"
    formatted_seq = ""
    for i in range(0, len(sequence), line_width):
        formatted_seq += sequence[i:i + line_width] + "\n"
    return header + "\n" + formatted_seq


def transcribe_sequence(sequence: str) -> str:
    """Returns the mRNA sequence by replacing T with U (in silico transcription)."""
    return sequence.replace('T', 'U').replace('t', 'u')


def complement_sequence(sequence: str) -> str:
    """Returns the complementary DNA strand (5'->3', same direction as input)."""
    complement_map = str.maketrans('ACGTacgt', 'TGCAtgca')
    return sequence.translate(complement_map)


def reverse_complement_sequence(sequence: str) -> str:
    """Returns the reverse complementary strand (antiparallel complement, 3'->5' read as 5'->3')."""
    return complement_sequence(sequence)[::-1]


def find_motif(sequence: str, motif: str) -> list[int]:
    """Returns all 1-based positions where the motif occurs in the sequence."""
    positions = []
    start = 0
    while True:
        pos = sequence.find(motif, start)
        if pos == -1:
            break
        positions.append(pos + 1)
        start = pos + 1
    return positions


def print_stats(stats: dict) -> None:
    """Prints nucleotide statistics """
    print(f"A: {stats['A']} %")
    print(f"C: {stats['C']} %")
    print(f"G: {stats['G']} %")
    print(f"T: {stats['T']} %")
    print(f"GC-content: {stats['GC']} %")



def validate_positive_int(input_str: str,
                           min_val: int = 1,
                           max_val: int = 100_000) -> int:
    """Prompts until the user enters an integer within [min_val, max_val]."""
    while True:
        try:
            value = int(input(input_str))
            if min_val <= value <= max_val:
                return value
            print(f"Error: value must be between [{min_val}, {max_val}].")
        except ValueError:
            print("Error: Please enter a valid integer.")


def ask_seq_id() -> str:
    """Input of sequence ID"""
    while True:
        seq_id = input("Input sequence ID (no whitespace): ").strip()
        if seq_id and ' ' not in seq_id and '\t' not in seq_id:
            return seq_id
        print("Error: ID cannot contain whitespace.")


def ask_output_file(default: str) -> str:
    """Prompts for an output filename and returns the full .fasta path"""
    output_file = input(
        f"Input output file name (without extension, default '{default}'): "
    ).strip()
    if not output_file:
        output_file = default
    return f"{output_file.replace(' ', '_')}.fasta"


def choose_mode() -> str:
    """Prompts the user to choose a generation mode."""
    while True:
        choice = input(
            "Choose mode:\n"
            "  [1] single sequence\n"
            "  [2] batch multi-FASTA\n"
            "  [3] complement (original + complement + reverse complement)\n"
            "  [4] transcription (DNA + mRNA)\n"
            "  [5] motif search\n"
            "Your choice: "
        ).strip()
        match choice:
            case '1' | 'single' | 's':
                return 'single'
            case '2' | 'batch' | 'b':
                return 'batch'
            case '3' | 'complement' | 'c':
                return 'complement'
            case '4' | 'transcription':
                return 'transcription'
            case '5' | 'motif' | 'm':
                return 'motif'
            case _:
                print("Error: choose 1–5 or type the mode name.")



def generate_single_fasta(length: int, seq_id: str,
                           description: str, name: str,
                           output_filename: str) -> None:
    """Generate a single FASTA record and write it to a file."""
    sequence = generate_sequence(length)
    sequence_with_name = insert_name(sequence, name)

    with open(output_filename, 'w') as f:
        f.write(format_fasta(seq_id, description, sequence_with_name))

    print(f"\nSequence saved to file: {output_filename}")
    print("\nSequence statistics:")
    print_stats(calculate_stats(sequence))


def generate_batch_fasta(batch_count: int, length: int,
                          description: str, output_filename: str) -> None:
    """Generate multiple FASTA records in a single multi-FASTA file."""
    fasta_records = ""
    digit_width = len(str(batch_count))

    for index in range(1, batch_count + 1):
        seq_id = f"Seq_{index:0{digit_width}d}"
        sequence = generate_sequence(length)
        fasta_records += format_fasta(seq_id, description, sequence)

        stats = calculate_stats(sequence)
        print(f"{seq_id}: A={stats['A']}%, C={stats['C']}%, "
              f"G={stats['G']}%, T={stats['T']}%, GC={stats['GC']}%")

    with open(output_filename, 'w') as f:
        f.write(fasta_records)


def generate_complement_fasta(length: int, seq_id: str,
                               description: str, output_filename: str) -> None:
    """Generate original, complementary, and reverse complementary FASTA records in one file."""
    sequence = generate_sequence(length)

    fasta_content = format_fasta(seq_id, description, sequence)
    fasta_content += format_fasta(f"{seq_id}_complement", description,
                                  complement_sequence(sequence))
    fasta_content += format_fasta(f"{seq_id}_revcomp", description,
                                  reverse_complement_sequence(sequence))

    with open(output_filename, 'w') as f:
        f.write(fasta_content)

    print(f"\nThree records saved to file: {output_filename}")
    print(f"  Records: {seq_id}, {seq_id}_complement, {seq_id}_revcomp")
    print("\nOriginal sequence statistics:")
    print_stats(calculate_stats(sequence))


def generate_transcription_fasta(length: int, seq_id: str,
                                  description: str, output_filename: str) -> None:
    """Generate a DNA sequence and its mRNA transcript as two FASTA records."""
    sequence = generate_sequence(length)

    fasta_content = format_fasta(seq_id, description, sequence)
    fasta_content += format_fasta(f"{seq_id}_mRNA", description,
                                  transcribe_sequence(sequence))

    with open(output_filename, 'w') as f:
        f.write(fasta_content)

    print(f"\nTwo records saved to file: {output_filename}")
    print(f"  Records: {seq_id} (DNA), {seq_id}_mRNA (mRNA)")
    print("\nDNA sequence statistics:")
    print_stats(calculate_stats(sequence))


def generate_motif_fasta(length: int, seq_id: str,
                          description: str, motif: str,
                          output_filename: str) -> None:
    """Generate a sequence, search for a motif, and save as a FASTA record."""
    sequence = generate_sequence(length)

    with open(output_filename, 'w') as f:
        f.write(format_fasta(seq_id, description, sequence))

    positions = find_motif(sequence, motif)
    print(f"\nSequence saved to file: {output_filename}")
    print(f"\nMotif '{motif}' search results:")
    if positions:
        print(f"  Found {len(positions)} occurrence(s) at position(s): "
              f"{', '.join(map(str, positions))}")
    else:
        print("  Motif not found in the sequence.")
    print("\nSequence statistics:")
    print_stats(calculate_stats(sequence))


def main():
    mode = choose_mode()

    match mode:
        case 'single':
            length = validate_positive_int("Input sequence length in range (1-100000): ")
            seq_id = ask_seq_id()
            description = input("Input sequence description (optional): ").strip()
            name = input("Input your name: ").strip()
            output_filename = ask_output_file("sequence")
            generate_single_fasta(length, seq_id, description, name, output_filename)

        case 'batch':
            batch_count = validate_positive_int(
                "Input number of sequences to generate: ", min_val=1, max_val=1000)
            length = validate_positive_int("Input sequence length in range (1-100000): ")
            description = input("Input sequence description (optional): ").strip()
            output_filename = ask_output_file("multi_sequences")
            generate_batch_fasta(batch_count, length, description, output_filename)
            print(f"\nGenerated {batch_count} sequences and saved them to file: {output_filename}")

        case 'complement':
            length = validate_positive_int("Input sequence length in range (1-100000): ")
            seq_id = ask_seq_id()
            description = input("Input sequence description (optional): ").strip()
            output_filename = ask_output_file("complement")
            generate_complement_fasta(length, seq_id, description, output_filename)

        case 'transcription':
            length = validate_positive_int("Input sequence length in range (1-100000): ")
            seq_id = ask_seq_id()
            description = input("Input sequence description (optional): ").strip()
            output_filename = ask_output_file("transcription")
            generate_transcription_fasta(length, seq_id, description, output_filename)

        case 'motif':
            length = validate_positive_int("Input sequence length in range (1-100000): ")
            seq_id = ask_seq_id()
            description = input("Input sequence description (optional): ").strip()
            motif = input("Input motif to search (e.g. ATG): ").strip().upper()
            output_filename = ask_output_file("motif_search")
            generate_motif_fasta(length, seq_id, description, motif, output_filename)


if __name__ == "__main__":
    main()
