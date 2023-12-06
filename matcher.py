# function implementation of matcher.ipynb
# input is array containing all fingerprint names and indirect feature vectors
# output is array containing nC2 combinations of fingerprint names and their similarity score

import matcherfunc as mf
import numpy as np
from pathlib import Path
from itertools import combinations


def  get_finger_id(name):
    # splits the path by '_' and returns the 2nd last value
    return int(Path(name).stem.split('_')[-2])

def match(db_array, T1, T2, denom_type = 'harmonic', dist_type = 'euclidean_norm'):
    """
    Calculate the similarity scores between fingerprints in the given database array.
    The genuine and imposter pairs are generated here.
    Args:
        db_array (list): The array containing the fingerprints. [[name, features_array],...]
        T1 (float): The first threshold value for alpha for matching.
        T2 (float): The second threshold value for thetha for matching.
        denom_type (str, optional): The type of matching to be performed. Can be one of 'harmonic', 'average', 'min', or 'geometric'. Defaults to 'min'.
        dist_type (str, optional): The type of distance to be used. Can be one of 'euclidean_norm' or 'euclidian_log_norm'. Defaults to 'euclidian_log_norm'.
    Returns:
        list: The similarity array containing the scores and flags for each pair of fingerprints.
    """
    # create array to store similarity scores
    # array stores score and flag for each pair of fingerprints
    # score is percentage matching of two vector arrays
    # flag is True if instance of same fingerprint, false otherwise
    # DONE: Update genuine pairs logic, imposter pair logic...
    person_feature_dict = {}
    for path,fv in db_array:
        id=get_finger_id(path)
        try:
            person_feature_dict[id].append(fv)
        except KeyError:
            person_feature_dict[id]=[fv]

    def nC2(fvs):
        for pair in combinations(fvs):
            yield pair

    def chain(arrs,func=nC2):
        for arr in arrs:
            if func is None:
                yield from arr
            else:
                yield from nC2(arr)

    def get_imposter(n_finger_per_person=1):
        for i in range(n_finger_per_person):
            yield (fp[i] for fp in person_feature_dict.values())
    
    genine_pairs = chain(person_feature_dict.values())
    n_finger_per_person = 3
    imposter_pairs = chain(get_imposter(n_finger_per_person))

    def get_denom(l1,l2,denom_type=denom_type):
        if denom_type == 'average':
            return (l1 + l2)/2
        if denom_type == 'geometric':
            return np.sqrt(l1*l2)
        if denom_type == 'harmonic':
            return 2*l1*l2/(l1 + l2)
        if denom_type == 'min':
            return min(l1, l2)
        else:
            raise Exception("Invalid denom_type, please enter one of {average, geometric, harmonic, min}")
    
    def get_score(pair):
        fp1,fp2 = pair
        l1,l2 = len(fp1,fp2)
        comb_arr = sorted(
            chain([
                    ((1,fv) for fv in fp1),
                    ((0,fv) for fv in fp2)
                ],None), key=lambda x:x[1]
            )
        # https://stackoverflow.com/questions/45655987/efficient-solution-for-merging-2-sorted-lists-in-python
        index_arr = sorted(
            ((i,fv[1]) for i,fv in enumerate(comb_arr) if fv[0]),
            key=lambda x:abs(x[1]))
        score = 0
        for index,_ in index_arr:
            score += mf.find_match(comb_arr,index,T1,T2,dist_type)
        percentage = (score / get_denom(l1,l2)) * 100
        return percentage

    tr_arr = sorted(get_score(pair) for pair in genine_pairs)
    fa_arr = sorted(get_score(pair) for pair in imposter_pairs)
    return tr_arr, fa_arr
    # for i in range(n):
    #     for j in range(i+1, n):
    #         # fp1 and fp2 are indirect feature vectors of two fingerprints
    #         fp1 = db_array[i][1]
    #         fp2 = db_array[j][1]

    #         array, index_array, length1, length2 = mf.combine_dataframes(fp1, fp2)
            

    #         # initialize score counter
    #         score = 0

    #         # check if fingerprint is same
    #         is_same = mf.check_name(db_array[i][0], db_array[j][0])

    #         # find order of index to scan
    #         index = mf.find_next_index(array, index_array)

    #         # calculate score
    #         for k in range(len(index_array)):
    #             # TODO: make score value into a gradient instead of boolean
    #             # work on the flag return value of find_match
    #             score += mf.find_match(array, index[k], T1, T2, dist_type)
            
    #         percentage = score/denom * 100
    #         # results.append([is_same, percentage])
    #         similarity_array.append([is_same, percentage])

    # return similarity_array

    # # incomplete
    # # TODO: may wanna complete this
    # import generatefeatures as gf
    # def balanced_dataset_generator(db_array, T1, T2, seed_count = 3):
    #     # split db_array into fingerprint_count number of arrays of size impression_count
    #     # call match function on each array
    #     new_db_array = gf.generatefeatures(db_array, seed_count)
    #     similarity_array = []
    #     for i in range(fingerprint_count):
    #         temp_array = []
    #         for j in range(impression_count):
    #             temp_array.append(db_array[i*impression_count + j])
    #         similarity_array.append(match(temp_array, T1, T2))
