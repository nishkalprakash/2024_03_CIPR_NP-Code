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

def match(db_array, T1, T2, denom_type = 'harmonic', dist_type = 'euclidean_norm', n_finger_per_person = 1):
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
        for pair in combinations(fvs,2):
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
    n_finger_per_person = 10
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
        l1,l2 = len(fp1),len(fp2)
        comb_arr = sorted(
            chain([
                    ([1]+fv for fv in fp1),
                    ([0]+fv for fv in fp2)
                ],None), key=lambda x:x[1]
            )
        # https://stackoverflow.com/questions/45655987/efficient-solution-for-merging-2-sorted-lists-in-python
        index_arr = sorted(
            ((i,flag_fv[1]) for i,flag_fv in enumerate(comb_arr) if flag_fv[0]),
            key=lambda x:abs(x[1]))
        score = 0
        index_gen = (i[0] for i in index_arr)
        for index in index_gen:
            sc = mf.get_match_score_at_index(index,comb_arr,T1,T2,dist_type)
            assert 0<=sc<=1,f"{sc} - ERROR: score not between 0 & 1"
            score+=sc

        percentage = (score / get_denom(l1,l2)) * 100
        return percentage

    tr_arr = sorted(get_score(pair) for pair in genine_pairs)
    fa_arr = sorted(get_score(pair) for pair in imposter_pairs)
    return tr_arr, fa_arr, list(genine_pairs), list(imposter_pairs)
