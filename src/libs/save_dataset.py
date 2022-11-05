import pandas as pd
import itertools
AMINO_SET = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K',
             'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'}


# protein_sequence_processing returns pd.Series of the number of subsequence of protein.
# the length of subsequence is length.
def protein_sequence_processing(protein_seq, length=1):
    protein_sequence_dict = dict()
    for seq in itertools.product(AMINO_SET, repeat=length):
        seq = "".join(seq)
        if seq[::-1] not in protein_sequence_dict:
            protein_sequence_dict[seq] = 0
    for start_idx in range(len(protein_seq)):
        protein_sub_sequence = [
            protein_seq[(start_idx+i) % len(protein_seq)] for i in range(length)]
        protein_sub_sequence = "".join(protein_sub_sequence)
        if protein_sequence_dict.get(protein_sub_sequence) is not None:
            protein_sequence_dict[protein_sub_sequence] += 1
        else:
            protein_sequence_dict[protein_sub_sequence[::-1]] += 1

    protein_sequence_series = pd.Series(
        data=protein_sequence_dict, index=sorted(protein_sequence_dict))

    return protein_sequence_series
