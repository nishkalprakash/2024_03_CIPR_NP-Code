# write a function that calculates the matching score of 2 dataframes
# columns of the dataframes are Log Ratio, Theta 1, Theta 2, Theta 3

import numpy as np
# import pandas as pd

# find match
# if match found, update flag for both indices to 2 and return 1
# if no match found, update flag for current index to 1 and return 0
def get_match_score_at_index(index, array, t1, t2, dist_type='euclidean_norm'):
    def diff(a,b):
        return abs(a-b)
    
    def alpha_within_thresh(match_index,index=index,array=array,t1=t1):
        if match_index is None:
            return False
        return diff(array[match_index][1],array[index][1])<t1
    
    def find_next_index(curr_index, direction='up', index=index, array=array):
        # direction can be 'up' or 'down'
        if direction == 'up':
            # Iterate up/backward to find the closest index with flag 1
            index_range = range(curr_index - 1, -1, -1)
        else:
            # Iterate down/forward to find the closest indext with flag 1
            index_range = range(curr_index + 1, len(array))
        for next_index in index_range:
            if array[next_index][0] == 1:
                if alpha_within_thresh(next_index, index):  
                    # Check if the element has flag 1 and within thresh
                    return next_index  # Found the closest index above
                else:
                    return None
        # end of array in the given direction, no next found
        return None  

    def get_row_match_score(r1_index, r2_index=index,array=array,t1=t1,t2=t2,dist_type=dist_type):
        """
        Calculates the row_match_score between two elements based on their attributes.

        Parameters:
        t1 (float): Threshold value for the alpha part of the score calculation.
        t2 (float): Threshold value for the theta part of the score calculation.
        mode (str, optional): Mode of calculation. Defaults to 'distance'.

        Returns:
        float: row_match_score score between the two row elements.
        """
        r1=array[r1_index]
        r2=array[r2_index]
        theta_part = 0
        if dist_type == 'euclidean_norm':
            alpha_part = np.sqrt((r1[1] - r2[1]) ** 2) / t1
        elif dist_type == 'euclidean_log_norm':
            # here the alpha part gets a inverse weightage based on the distance from 0, so values close to 0 gets a higher weightage
            alpha_part = (np.sqrt((r1[1] - r2[1]) ** 2) / t1) * 1 / np.sqrt(1 + abs(r1[1]) + abs(r2[1]))
        elif dist_type == 'euclidean_log_norm_hack':
            alpha_part = (np.sqrt((r1[1] - r2[1]) ** 2) / t1) * 1 / (1 + abs(r1[1]) + abs(r2[1]))**0.2
        else:
            raise Exception("Invalid dist_type, please enter one of {euclidean_norm, euclidean_log_norm, euclidean_log_norm_hack}")
        theta_part = np.sqrt((r1[2] - r2[2]) ** 2 + (r1[3] - r2[3]) ** 2 + (r1[4] - r2[4]) ** 2) / (1.7321 * t2)
        return 1 - (alpha_part + 3 * theta_part) / 4
         
    def thetas_within_thresh(r1_index, r2_index=index,array=array,t1=t1,t2=t2):
        r1=array[r1_index]
        r2=array[r2_index]
        # if diff(r1[1],r2[1]) < t1: # no need to check for alpha
        # TODO: check if this constraint can be fixed
        if diff(r1[2],r2[2]) < t2 and diff(r1[3],r2[3]) < t2 and diff(r1[4],r2[4]) < t2:
            return True
        return False

    def update_flags(match_index,index=index,array=array):
        # Helper function to update flags
        if match_index:
            array[match_index][0] = 2
        array[index][0] = 2

    def get_match_index(next_up_index,next_down_index,index=index,array=array):
        # if both exist, pick having smaller alpha
        if next_up_index and next_down_index:
            # if down is smaller
            if diff(array[next_down_index][1], array[index][1]) < diff(array[index][1],array[next_up_index][1]):
                return next_down_index
            return next_up_index
        return next_up_index or next_down_index

    index_up = index
    index_down = index
    match_index = index
    while match_index:
        if match_index == index_up:
            index_up = find_next_index(index_up,'up')
        if match_index == index_down:
            index_down = find_next_index(index_down,'down')
        match_index = get_match_index(index_up,index_down)
        if match_index:
            if thetas_within_thresh(match_index):
                update_flags(match_index)
                return get_row_match_score(match_index)
                # return 1
            # else the loop continues to find_next_index to match with
    # No match found within the threshold, update current index and proceed
    update_flags(match_index)
    return 0