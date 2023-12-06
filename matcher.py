# function implementation of matcher.ipynb
# input is array containing all fingerprint names and indirect feature vectors
# output is array containing nC2 combinations of fingerprint names and their similarity score

import matcherfunc as mf

def match(db_array, threshold1, threshold2):
    # find length of array to know number of fingerprints
    n = len(db_array)

    # create array to store similarity scores
    # array stores score and flag for each pair of fingerprints
    # score is percentage matching of two vector arrays
    # flag is True if instance of same fingerprint, false otherwise
    similarity_array = []
    # TODO: Update genuine pairs logic, imposter pair logic...
    # iterate through all combinations of fingerprints
    for i in range(n):
        for j in range(i+1, n):
            # fp1 and fp2 are indirect feature vectors of two fingerprints
            fp1 = db_array[i][1]
            fp2 = db_array[j][1]

            array, flag, length1, length2 = mf.combine_dataframes(fp1, fp2)
            denom = min(length1, length2)

            # initialize score counter
            score = 0

            # check if fingerprint is same
            is_same = mf.check_name(db_array[i][0], db_array[j][0])

            # find order of index to scan
            index = mf.find_next_index(array, flag)

            # calculate score
            for k in range(len(flag)):
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