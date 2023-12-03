# return the best array matching threshold for a given pair of thresholds

import numpy as np

# splitting and counting the array based on true and false flag
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

    # find the values at which score is n for both arrays and report (index + 1) / len(array) for both arrays
    # n in range 2o to 80
    true_length = len(trarr)
    cumulative_true = []
    n = 0
    for i in range(true_length):
        if n > 80:
            break
        while trarr[i] <= n:
            i += 1
            if i >= len(trarr):
                break
        cumulative_true.append(i)
        n += 1

    false_length = len(faarr)
    cumulative_false = []
    n = 0
    for i in range(false_length):
        if n > 80:
            break
        while faarr[i] <= n:
            i += 1
            if i >= len(faarr):
                break
        cumulative_false.append(i)
        n += 1
    return cumulative_true, cumulative_false, true_length, false_length

def calc_precision(tp, tn, fp, fn):
    if tp + fp == 0:
        return 0
    return tp / (tp + fp)
def calc_recall(tp, tn, fp, fn):
    if tp + fn == 0:
        return 0
    return tp / (tp + fn)

def calculate_far(similarity_array, threshold1, threshold2):

    def calc_far(tp, tn, fp, fn):
        return 1 - calc_precision(tp, tn, fp, fn)
        # pre = calc_precision(tp, tn, fp, fn)
        # rec = calc_recall(tp, tn, fp, fn)
        # if pre == 0 or rec == 0:
        #     return 0
        # return 2 * pre * rec / (pre + rec)
    
    cumulative_true, cumulative_false, true_length, false_length = preprocess(similarity_array)

    # maximize f1 score
    f1 = 0
    threshold = 0
    # store conditions when f1 score is maximum
    for i in range(0, 81):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        # print(tp, tn, fp, fn)
        f1_score = calc_far(tp, tn, fp, fn)
        if f1_score > f1:
            f1 = f1_score
            threshold = i
    return [threshold1, threshold2, threshold, f1]

def calculate_frr(similarity_array, threshold1, threshold2):

    def calc_frr(tp, tn, fp, fn):
        frr = fn/(tp + tn + fp + fn)
        # rec = calc_recall(tp, tn, fp, fn)
        # if pre == 0 or rec == 0:
        #     return 0
        # return 2 * pre * rec / (pre + rec)
    
    cumulative_true, cumulative_false, true_length, false_length = preprocess(similarity_array)

    # maximize f1 score
    f1 = 0
    threshold = 0
    # store conditions when f1 score is maximum
    for i in range(0, 81):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        # print(tp, tn, fp, fn)
        f1_score = calc_frr(tp, tn, fp, fn)
        if f1_score > f1:
            f1 = f1_score
            threshold = i
    return [threshold1, threshold2, threshold, f1]
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
    for i in range(0, 81):
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
    for i in range(0, 81):
        fn = cumulative_true[i]
        tn = cumulative_false[i]
        fp = false_length - tn
        tp = true_length - fn
        MCC_score = calc_MCC_score(tp, tn, fp, fn)
        if MCC_score > MCC:
            MCC = MCC_score
            threshold = i
    return [threshold1, threshold2, threshold, MCC]