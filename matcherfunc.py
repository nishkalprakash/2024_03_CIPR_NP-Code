# write a function that calculates the matching score of 2 dataframes
# columns of the dataframes are Log Ratio, Theta 1, Theta 2, Theta 3

import numpy as np
import pandas as pd

def find_next_index(array, flag):
    # return an array that stores the indices in increasing absolute value of log ratio
    # only indices of array needed are stored in flag array
    # array is a list of elements with 5 parameters
    # log ratio is second parameter

    list1 = []
    for i in range(len(flag)):
        list1.append([flag[i], array[flag[i]][1]])
    list1.sort(key=lambda x: abs(x[1]))

    list2 = []
    for i in range(len(list1)):
        list2.append(list1[i][0])
    
    return list2


def check_name(name1, name2):
    # split name1 and name2 into tokens based on '_'
    # check if all tokens except the last one are the same
    # if yes, return True
    # if no, return False
    name1 = name1.split('_')
    name2 = name2.split('_')
    if len(name1) != len(name2):
        return False
    else:
        for i in range(len(name1)-1):
            if name1[i] != name2[i]:
                return False
        return True


def combine_dataframes(df1, df2):
    length = len(df1)
    length2 = len(df2)

    flag0 = []

    array = []

    j, k = 0, 0
    for i in range(len(df1)+len(df2)):
        if j == len(df1):
            array.append([1, df2[k][0], df2[k][1], df2[k][2], df2[k][3]])
            k += 1
        elif k == len(df2):
            array.append([0, df1[j][0], df1[j][1], df1[j][2], df1[j][3]])
            j += 1
            flag0.append(i)
        elif df1[j][0] < df2[k][0]:
            array.append([0, df1[j][0], df1[j][1], df1[j][2], df1[j][3]])
            j += 1
            flag0.append(i)
        else:
            array.append([1, df2[k][0], df2[k][1], df2[k][2], df2[k][3]])
            k += 1
    
    return array, flag0, length, length2



# find match
# if match found, update flag for both indices to 2 and return 1
# if no match found, update flag for current index to 1 and return 0
def find_match(array, index, t1, t2, dist_type='euclidean_norm'):

    def find_closest_above(array, index):
        # Iterate backward to find the closest index above with flag 1
        for i in range(index - 1, -1, -1):
            if array[i][0] == 1:  # Check if the element has flag 1
                return i  # Found the closest index above

        return None  # No index with flag 1 found above


    def find_closest_below(array, index):
        # iterate forward to find the closest index below with flag 1
        for i in range(index + 1, len(array)):
            if array[i][0] == 1:  # Check if the element has flag 1
                return i  # Found the closest index below    
        return None  # No index with flag 1 found below

    def get_row_match_score(r1, r2):
        """
        Calculates the row_match_score between two elements based on their attributes.

        Parameters:
        r1 (list): List of attributes for the first element.
        r2 (list): List of attributes for the second element.
        t1 (float): Threshold value for the alpha part of the score calculation.
        t2 (float): Threshold value for the theta part of the score calculation.
        mode (str, optional): Mode of calculation. Defaults to 'distance'.

        Returns:
        float: row_match_score score between the two row elements.
        """
        if dist_type == 'euclidean_norm':
            alpha_part = np.sqrt((r1[1] - r2[1]) ** 2) / t1
            # theta_part = np.sqrt((r1[2] - r2[2]) ** 2 + (r1[3] - r2[3]) ** 2 + (r1[4] - r2[4]) ** 2) / (1.7321 * t2)
        
        elif dist_type == 'euclidian_log_norm':
            # here the alpha part gets a inverse weightage based on the distance from 0, so values close to 0 gets a higher weightage
            alpha_part = (np.sqrt((r1[1] - r2[1]) ** 2) / t1) * 1 / np.sqrt(1 + abs(r1[1]) + abs(r2[1]))
            # theta_part = np.sqrt((r1[2] - r2[2]) ** 2 + (r1[3] - r2[3]) ** 2 + (r1[4] - r2[4]) ** 2) / (1.7321 * t2)
            # return 1 - (alpha_part + 3 * theta_part) / 4    
        
        elif dist_type == 'euclidian_log_norm_hack':
            alpha_part = (np.sqrt((r1[1] - r2[1]) ** 2) / t1) * 1 / (1 + abs(r1[1]) + abs(r2[1]))**0.2
            # theta_part = np.sqrt((r1[2] - r2[2]) ** 2 + (r1[3] - r2[3]) ** 2 + (r1[4] - r2[4]) ** 2) / (1.7321 * t2)
            # return 1 - (alpha_part + 3 * theta_part) / 4
        
        else:
            raise Exception("Invalid dist_type, please enter one of {euclidean_norm, euclidian_log_norm, euclidian_log_norm_hack}")
        theta_part = np.sqrt((r1[2] - r2[2]) ** 2 + (r1[3] - r2[3]) ** 2 + (r1[4] - r2[4]) ** 2) / (1.7321 * t2)
        return 1 - (alpha_part + 3 * theta_part) / 4
         
        
    def match_function(r1, r2):
        if abs(r1[1]-r2[1]) < t1:
            if abs(r1[2]-r2[2]) < t2 and abs(r1[3]-r2[3]) < t2 and abs(r1[4]-r2[4]) < t2:
                return True
            else:
                return False
        else:
            return False

    # if match found, update row_match_score for both indices and return 1
    # if no match found, update row_match_score for current index and return 0

    def update_flags(current_index, closest_index):
        # Helper function to update flags and perform other processing
        array[current_index][0] = 2
        array[closest_index][0] = 2

    index_up = index
    index_down = index
    row_match_score = 0

    while True:
        closest_above_index = find_closest_above(array, index_up)
        closest_below_index = find_closest_below(array, index_down)

        # check if threshold is reached
        if closest_above_index is not None:
            if abs(array[closest_above_index][1] - array[index][1]) > t1:
                closest_above_index = None
        
        if closest_below_index is not None:
            if abs(array[closest_below_index][1] - array[index][1]) > t1:
                closest_below_index = None

        # Check if there's a closest index above and below
        if closest_above_index is not None and closest_below_index is not None:
            # if above is closer than below
            if array[closest_below_index][1] - array[index][1] > array[index][1] - array[closest_above_index][1]:
                # Check if the closest index above is within the threshold
                if match_function(array[index], array[closest_above_index]):
                    # Match found, update flags or do other processing
                    update_flags(index, closest_above_index)
                    row_match_score = get_row_match_score(array[index], array[closest_above_index]) # Set row_match_score to score to indicate a match is found
                    return row_match_score
            else:
                # Check if the closest index below is within the threshold
                if match_function(array[index], array[closest_below_index]):
                    # Match found, update flags or do other processing
                    update_flags(index, closest_below_index)
                    row_match_score = get_row_match_score(array[index], array[closest_below_index]) # Set row_match_score to score to indicate a match is found
                    return row_match_score

        # if only above is not None
        elif closest_above_index is not None:
            # Check if the closest index above is within the threshold
            if match_function(array[index], array[closest_above_index]):
                # Match found, update flags or do other processing
                update_flags(index, closest_above_index)
                row_match_score = get_row_match_score(array[index], array[closest_above_index]) # Set row_match_score to score to indicate a match is found
                return row_match_score

        # if only below is not None
        elif closest_below_index is not None:
            # Check if the closest index below is within the threshold
            if match_function(array[index], array[closest_below_index]):
                # Match found, update flags or do other processing
                update_flags(index, closest_below_index)
                row_match_score = get_row_match_score(array[index], array[closest_below_index]) # Set row_match_score to score to indicate a match is found
                return row_match_score

        # No match found within the threshold, update row_match_score for current index and proceed
        else:
            array[index][0] = 2
            row_match_score = 0
            # break
            return row_match_score

        # if either above or below not none but still no match found
        # update index_up and index_down without changing index andd loop

        if closest_above_index is not None:
            index_up = closest_above_index

        if closest_below_index is not None:
            index_down = closest_below_index
    
    return row_match_score