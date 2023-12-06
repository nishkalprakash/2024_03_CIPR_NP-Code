# return the best array matching threshold for a given pair of thresholds

import numpy as np

# splitting and counting the array based on true and false flag
# TODO: change cumulative_true and cumulative_false to more fine grained percentages
"""""
created grain_traversal and block_traversal
call calculate_block_far_frr_score for 1% check
call calculate_grain_far_frr_score for 0.1% check
@nishkalpraksah check
"""""

def preprocess(array):
    trarr = []
    faarr = []
    for i in range(len(array)):
        if array[i][0]:
            trarr.append(array[i][1])
        else:
            faarr.append(array[i][1])

    # sort the arrays based on score column
    trarr.sort()
    faarr.sort()

    return trarr, faarr

def traverse(tr_arr,fa_arr,gr=0.1):
    def get_cumlative_array(array):
        # find the values at which score is n for both arrays and report (index + 1) / len(array) for both arrays
        # c_arr_l in range 0 to (100//gr)
        cumulative_arr = []
        c_arr_l = int(100/gr)
        arr_ptr,c_arr_ptr = 0,0
        arr_l = len(array)
        while arr_ptr < arr_l:
            # for arr_ptr in range(arr_l):
            if c_arr_ptr > c_arr_l: # if c_arr_ptr is greater than limit, break
                break
            while array[arr_ptr] <= c_arr_ptr*gr:
                arr_ptr += 1
                if arr_ptr >= arr_l:
                    break
            if arr_ptr < arr_l:
                while c_arr_ptr*gr < array[arr_ptr]:
                    cumulative_arr.append(arr_ptr)
                    c_arr_ptr += 1
        # here there is no more elements in array, so complete the cumulative array to lenth c_arr_l
        while c_arr_ptr<=c_arr_l:
            cumulative_arr.append(arr_l)
            c_arr_ptr += 1
        return cumulative_arr
    # tr_arr, fa_arr = preprocess(array)
    true_length = len(tr_arr)
    false_length = len(fa_arr)
    cumulative_true = get_cumlative_array(tr_arr)
    cumulative_false = get_cumlative_array(fa_arr)  
    return cumulative_true, cumulative_false, true_length, false_length

# DONE: make correct calc far and calc frr functions
def calculate_far_frr_score(t1, t2,tr_arr,fa_arr, gr=0.1):
    """
    Input:
        gr (granularity): 1 for block, 0.1 for grain
    Output:
            T1, T2, T3, FAR, FRR, EER
    """
    def calc_far_score(tp, tn, fp, fn):
       return fp/(tn+fp)
    
    def calc_frr_score(tp, tn, fp, fn):
        return fn/(tp+fn)
    
    
    cumulative_true, cumulative_false, true_length, false_length = traverse(tr_arr,fa_arr, gr)

    eer_opt=1
    t3 = 0
    far_opt, frr_opt = 0, 0
    for i in range(0, int(100/gr)+1):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        far_score = calc_far_score(tp, tn, fp, fn)
        frr_score = calc_frr_score(tp, tn, fp, fn)
        eer_score = (far_score + frr_score) / 2
        if eer_opt > eer_score:
            eer_opt = eer_score
            far_opt = far_score
            frr_opt = frr_score
            t3 = i
    return [t1, t2, t3, far_opt, frr_opt, eer_opt]

def calc_precision(tp, tn, fp, fn):
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)
def calc_recall(tp, tn, fp, fn):
    if tp + fn == 0:
        return 0
    return tp / (tp + fn)

# def calculate_f1_score(similarity_array, threshold1, threshold2):

#     def calc_f1_score(tp, tn, fp, fn):
#         pre = calc_precision(tp, tn, fp, fn)
#         rec = calc_recall(tp, tn, fp, fn)
#         if pre == 0 or rec == 0:
#             return 0
#         return 2 * pre * rec / (pre + rec)
    
#     cumulative_true, cumulative_false, true_length, false_length = preprocess(similarity_array)

#     # maximize f1 score
#     f1 = 0
#     threshold = 0
#     # store conditions when f1 score is maximum
#     for i in range(0, 101):
#         fn = cumulative_true[i]
#         tn = cumulative_false[i]
#         fp = false_length - tn
#         tp = true_length - fn
#         # print(tp, tn, fp, fn)
#         f1_score = calc_f1_score(tp, tn, fp, fn)
#         if f1_score > f1:
#             f1 = f1_score
#             threshold = i
#     return [threshold1, threshold2, threshold, f1]

# def calculate_MCC_score(similarity_array, threshold1, threshold2):
    # MCC is defined as (TP*TN - FP*FN)/sqrt((TP+FP)*(TP+FN)*(TN+FP)*(TN+FN))

    def calc_MCC_score(tp, tn, fp, fn):
        if (tp + fp) == 0 or (tp + fn) == 0 or (tn + fp) == 0 or (tn + fn) == 0:
            return 0
        return (tp * tn - fp * fn) / np.sqrt((tp + fp) * (tp + fn) * (tn + fp) * (tn + fn))
    
    cumulative_true, cumulative_false, true_length, false_length = preprocess(similarity_array)

    # maximize MCC score
    MCC = 0
    threshold = 0
    # store conditions when MCC score is maximum
    for i in range(0, 101):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        MCC_score = calc_MCC_score(tp, tn, fp, fn)
        if MCC_score > MCC:
            MCC = MCC_score
            threshold = i
    return [threshold1, threshold2, threshold, MCC]