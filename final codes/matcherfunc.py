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
def find_match(array, index, threshold1, threshold2):

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



    def match_function(element1, element2, threshold1, threshold2):
        if abs(element1[1]-element2[1]) < threshold1:
            if abs(element1[2]-element2[2]) < threshold2 and abs(element1[3]-element2[3]) < threshold2 and abs(element1[4]-element2[4]) < threshold2:
                return True
        else:
            return False

    # if match found, update flag for both indices and return 1
    # if no match found, update flag for current index and return 0

    def update_flags(current_index, closest_index):
        # Helper function to update flags and perform other processing
        array[current_index][0] = 2
        array[closest_index][0] = 2

    index_up = index
    index_down = index
    flag = 0

    while True:
        closest_above_index = find_closest_above(array, index_up)
        closest_below_index = find_closest_below(array, index_down)

        # check if threshold is reached
        if closest_above_index is not None:
            if abs(array[closest_above_index][1] - array[index][1]) > threshold1:
                closest_above_index = None
        
        if closest_below_index is not None:
            if abs(array[closest_below_index][1] - array[index][1]) > threshold1:
                closest_below_index = None

        # Check if there's a closest index above and below
        if closest_above_index is not None and closest_below_index is not None:
            # if above is closer than below
            if array[closest_below_index][1] - array[index][1] > array[index][1] - array[closest_above_index][1]:
                # Check if the closest index above is within the threshold
                if match_function(array[index], array[closest_above_index], threshold1, threshold2):
                    # Match found, update flags or do other processing
                    update_flags(index, closest_above_index)
                    flag = 1 # Set flag to 1 to indicate a match is found
                    break  # Exit the loop
            else:
                # Check if the closest index below is within the threshold
                if match_function(array[index], array[closest_below_index], threshold1, threshold2):
                    # Match found, update flags or do other processing
                    update_flags(index, closest_below_index)
                    flag = 1 # Set flag to 1 to indicate a match is found
                    break  # Exit the loop

        # if only above is not None
        elif closest_above_index is not None:
            # Check if the closest index above is within the threshold
            if match_function(array[index], array[closest_above_index], threshold1, threshold2):
                # Match found, update flags or do other processing
                update_flags(index, closest_above_index)
                flag = 1 # Set flag to 1 to indicate a match is found
                break  # Exit the loop

        # if only below is not None
        elif closest_below_index is not None:
            # Check if the closest index below is within the threshold
            if match_function(array[index], array[closest_below_index], threshold1, threshold2):
                # Match found, update flags or do other processing
                update_flags(index, closest_below_index)
                flag = 1 # Set flag to 1 to indicate a match is found
                break  # Exit the loop

        # No match found within the threshold, update flag for current index and proceed
        else:
            array[index][0] = 2
            break

        # if either above or below not none but still no match found
        # update index_up and index_down without changing index andd loop

        if closest_above_index is not None:
            index_up = closest_above_index

        if closest_below_index is not None:
            index_down = closest_below_index
    
    return flag