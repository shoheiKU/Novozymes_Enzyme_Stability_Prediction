import itertools
import pandas as pd
import tqdm
from difflib import SequenceMatcher as SM
AMINO_SET = {'A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K',
             'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y'}


# input:
#   protein_seq: (str) a sequence of a protein,
#   longth: (int) the length of a subsequence (default=1)
# output:
#   protein_sequence_series: (pd.Series) the series of subsequence frequency of the protein.
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


# input:
#   dataset: (pd.DataFrame) input dataset,
#   length: (int) the dividing number of amino sequence (default=1)
# output:
#   dataset: (pd.Dataframe) dataset with the protein subsequence frequency
def to_amino_num_features_dataset(dataset: pd.DataFrame, length=1):
    amino_feature = pd.DataFrame()
    for protein_sequence in tqdm.tqdm(dataset['protein_sequence']):
        amino_series = protein_sequence_processing(protein_sequence, length)
        amino_feature = amino_feature.append(amino_series, ignore_index=True)
    return pd.concat([amino_feature, dataset['pH']], axis=1)

# input dataset: pd.DataFrame with 'protein_sequence'
# output dataset: pd.DataFrame added classified number, match_percent_threshold is the threshold of theconsistency rate.


def add_classified_num_dataset(dataset: pd.DataFrame, match_ratio_threshold=0.5):
    added_dataframe = pd.DataFrame(columns=['classified_number'])
    classified_number = 0
    original_sequence = dataset.at[dataset.index[0], 'protein_sequence']
    for index_num, protein_sequence in tqdm.tqdm(enumerate(dataset['protein_sequence'])):
        added_dataframe.at[dataset.index[index_num],
                           'classified_number'] = classified_number
        if SM(None, protein_sequence, original_sequence).ratio() < match_ratio_threshold:
            original_sequence = protein_sequence
            classified_number += 1
    return pd.concat([dataset, added_dataframe], axis=1)
