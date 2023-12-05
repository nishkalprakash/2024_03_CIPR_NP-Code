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

def traverse(array,gr=1):
    def get_cumlative_array(array, gr=1):
        # find the values at which score is n for both arrays and report (index + 1) / len(array) for both arrays
        # c_arr_l in range 0 to (100//gr)
        cumulative_arr = []
        c_arr_l = 100//gr
        c_arr_ptr = 0
        arr_l = len(array)
        for arr_ptr in range(arr_l):
            if c_arr_ptr > c_arr_l: # if c_arr_ptr is greater than limit, break
                break
            while array[arr_ptr] <= c_arr_ptr*gr:
                arr_ptr += 1
                if arr_ptr >= arr_l:
                    break
            while c_arr_ptr*gr < array[arr_ptr]:
                cumulative_arr.append(arr_ptr)
                c_arr_ptr += 1
        return cumulative_arr
    true_array, false_array = preprocess(array)
    true_length = len(true_array)
    false_length = len(false_array)
    cumulative_true = get_cumlative_array(true_array, gr)
    cumulative_false = get_cumlative_array(false_array, gr)
    # n = 0
    # # TODO: fix this for the required logic for cumulative array creation
    # # @nishkalprakash check this
    # for i in range(true_length):
    #     if n > cumulative_array_length:
    #         break
    #     while true_array[i] <= n:
    #         i += 1
    #         if i >= len(true_array):
    #             break
    #     # for j in    
    #     # TODO: fix this
    #     # Check this @nishkalprakash
    #     while n*gr < true_array[i]:
    #         cumulative_true.append(i)
    #         n += 1

    
    return cumulative_true, cumulative_false, true_length, false_length

# def block_traverse(array):
#     true_array, false_array = preprocess(array)
#     # find the values at which score is n for both arrays and report (index + 1) / len(array) for both arrays
#     # n in range 0 to 100
#     true_length = len(true_array)
#     cumulative_true = []
#     n = 0
#     # TODO: fix this for the required logic for cumulative array creation
#     # @nishkalprakash check this
#     for i in range(true_length):
#         if n > 100:
#             break
#         while true_array[i] <= n:
#             i += 1
#             if i >= len(true_array):
#                 break
#         # for j in    
#         # TODO: fix this
#         # Check this @nishkalprakash
#         while n < true_array[i]:
#             cumulative_true.append(i)
#             n += 1

#     false_length = len(false_array)
#     cumulative_false = []
#     n = 0
#     for i in range(false_length):
#         if n > 100:
#             break
#         while false_array[i] <= n:
#             i += 1
#             if i >= len(false_array):
#                 break
#         while n < false_array[i]:
#             cumulative_false.append(i)
#             n += 1
#     return cumulative_true, cumulative_false, true_length, false_length

# def grain_traverse(array):
#     true_array, false_array = preprocess(array)
#     # find the values at which score is n for both arrays and report (index + 1) / len(array) for both arrays
#     # n in range 0 to 100
#     true_length = len(true_array)
#     cumulative_true = []
#     n = 0
#     # TODO: fix this for the required logic for cumulative array creation
#     # for ci in range(100):
#     #     cumulative_true.append()


#     for i in range(true_length):
#         if n > 1000:
#             break
#         while true_array[i] <= n/10:
#             i += 1
#             if i >= len(true_array):
#                 break
#         # for j in    
#         # TODO: fix this
#         # Check this @nishkalprakash
#         while n/10 < true_array[i]:
#             cumulative_true.append(i)
#             n += 1

#     false_length = len(false_array)
#     cumulative_false = []
#     n = 0
#     for i in range(false_length):
#         if n > 1000:
#             break
#         while false_array[i] <= n/10:
#             i += 1
#             if i >= len(false_array):
#                 break
#         while n/10 < false_array[i]:
#             cumulative_false.append(i)
#             n += 1
#     return cumulative_true, cumulative_false, true_length, false_length


# TODO: make correct calc far and calc frr functions
def calculate_far_frr_score(similarity_array, t1, t2, gr=1):
    # https://www.dicorm.com.my/post/demystifying-far-and-frr#:~:text=You%20calculate%20the%20FAR%20and,of%20true%20positives)%20x%20100
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
    
    
    cumulative_true, cumulative_false, true_length, false_length = traverse(similarity_array, gr=gr)

    # minimize avg of far and frr score
    # f1 = 0
    eer_opt=1
    t3 = 0
    far_opt, frr_opt = 0, 0
    # store conditions when f1 score is maximum
    for i in range(0, (100//gr)+1):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        # print(tp, tn, fp, fn)
        far_score = calc_far_score(tp, tn, fp, fn)
        frr_score = calc_frr_score(tp, tn, fp, fn)
        eer_score = (far_score + frr_score) / 2
        if eer_opt > eer_score:
            eer_opt = eer_score
            far_opt = far_score
            frr_opt = frr_score
            t3 = i
    return [t1, t2, t3, far_opt, frr_opt, eer_opt]

# def calculate_grain_far_frr_score(similarity_array, t1, t2):
#     # https://www.dicorm.com.my/post/demystifying-far-and-frr#:~:text=You%20calculate%20the%20FAR%20and,of%20true%20positives)%20x%20100
#     """
#     Input:

#     Output:
#             T1, T2, T3, FAR, FRR
#     """
#     def calc_far_score(tp, tn, fp, fn):
#        return fp/(tn+fp)
    
#     def calc_frr_score(tp, tn, fp, fn):
#         return fn/(tp+fn)

#     cumulative_true, cumulative_false, true_length, false_length = grain_traverse(similarity_array)

#     # minimize avg of far and frr score
#     # f1 = 0
#     temp=1
#     t3 = 0
#     far_opt, frr_opt = 0, 0
#     # store conditions when f1 score is maximum
#     for i in range(0, 1001):
#         fn = cumulative_true[i]
#         tn = cumulative_false[i]
#         fp = false_length - tn
#         tp = true_length - fn
#         # print(tp, tn, fp, fn)
#         far_score = calc_far_score(tp, tn, fp, fn)
#         frr_score = calc_frr_score(tp, tn, fp, fn)
#         eer_score = (far_score + frr_score) / 2
#         if temp > eer_score:
#             temp = eer_score
#             far_opt = far_score
#             frr_opt = frr_score
#             t3 = i/10
#     return [t1, t2, t3, far_opt, frr_opt, (far_opt + frr_opt) / 2]

def calc_precision(tp, tn, fp, fn):
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)
def calc_recall(tp, tn, fp, fn):
    if tp + fn == 0:
        return 0
    return tp / (tp + fn)

def calculate_f1_score(similarity_array, threshold1, threshold2):

    def calc_f1_score(tp, tn, fp, fn):
        pre = calc_precision(tp, tn, fp, fn)
        rec = calc_recall(tp, tn, fp, fn)
        if pre == 0 or rec == 0:
            return 0
        return 2 * pre * rec / (pre + rec)
    
    cumulative_true, cumulative_false, true_length, false_length = preprocess(similarity_array)

    # maximize f1 score
    f1 = 0
    threshold = 0
    # store conditions when f1 score is maximum
    for i in range(0, 101):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        # print(tp, tn, fp, fn)
        f1_score = calc_f1_score(tp, tn, fp, fn)
        if f1_score > f1:
            f1 = f1_score
            threshold = i
    return [threshold1, threshold2, threshold, f1]

def calculate_MCC_score(similarity_array, threshold1, threshold2):
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