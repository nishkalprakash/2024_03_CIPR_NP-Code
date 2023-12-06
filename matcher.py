# function implementation of matcher.ipynb
# input is array containing all fingerprint names and indirect feature vectors
# output is array containing nC2 combinations of fingerprint names and their similarity score

import matcherfunc as mf
import numpy as np

def match(db_array, threshold1, threshold2, match_type='min'):
    """
    Calculate the similarity scores between fingerprints in the given database array.
    The genuine and imposter pairs are generated here.
    Args:
        db_array (list): The array containing the fingerprints. [[name, features_array],...]
        threshold1 (float): The first threshold value for alpha for matching.
        threshold2 (float): The second threshold value for thetha for matching.
        match_type (str, optional): The type of matching to be performed. Can be one of 'harmonic', 'average', 'min', or 'geometric'. Defaults to 'min'.

    Returns:
        list: The similarity array containing the scores and flags for each pair of fingerprints.
    """
    
    # Rest of the code...
def match(db_array, threshold1, threshold2, match_type = 'min'):
    
    # """ match_type can be {harmonic, average, min, geometric} """

    # find length of array to know number of fingerprints
    n = len(db_array)

    # create array to store similarity scores
    # array stores score and flag for each pair of fingerprints
    # score is percentage matching of two vector arrays
    # flag is True if instance of same fingerprint, false otherwise
    similarity_array = []
    # TODO: Update genuine pairs logic, imposter pair logic...
    # iterate through all combinations of fingerprints
    

    # this loop takes all combinations of fingerprints
    # change to take only 450 genuine pairs and 450 imposter pairs
    for i in range(n):
        for j in range(i+1, n):
            # fp1 and fp2 are indirect feature vectors of two fingerprints
            fp1 = db_array[i][1]
            fp2 = db_array[j][1]

            array, flag, length1, length2 = mf.combine_dataframes(fp1, fp2)
            if match_type == 'average':
                denom = (length1 + length2)/2
            elif match_type == 'geometric':
                denom = np.sqrt(length1*length2)
            elif match_type == 'harmonic':
                denom = 2*length1*length2/(length1 + length2)
            elif match_type == 'min':
                denom = min(length1, length2)

            # initialize score counter
            score = 0

            # check if fingerprint is same
            is_same = mf.check_name(db_array[i][0], db_array[j][0])

            # find order of index to scan
            index = mf.find_next_index(array, flag)

            # calculate score
            for k in range(len(flag)):
                # TODO: make score value into a gradient instead of boolean
                # work on the flag return value of find_match
                score += mf.find_match(array, index[k], threshold1, threshold2)
            
            percentage = score/denom * 100
            # results.append([is_same, percentage])
            similarity_array.append([is_same, percentage])

    return similarity_array

# # incomplete
# # TODO: may wanna complete this
# import generatefeatures as gf
# def balanced_dataset_generator(db_array, threshold1, threshold2, seed_count = 3):
#     # split db_array into fingerprint_count number of arrays of size impression_count
#     # call match function on each array
#     new_db_array = gf.generatefeatures(db_array, seed_count)
#     similarity_array = []
#     for i in range(fingerprint_count):
#         temp_array = []
#         for j in range(impression_count):
#             temp_array.append(db_array[i*impression_count + j])
#         similarity_array.append(match(temp_array, threshold1, threshold2))