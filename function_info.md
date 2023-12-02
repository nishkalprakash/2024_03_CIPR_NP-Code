
thresholdtester.py
    contains 3 functions:
        calculate_f1_score
            input:
                array of results,
                threshold of log ratio,
                threshold of theta
            output:
                tuple [threshold of log ratio, threshold of theta, threshold of array match, F1 score]
        calculate_MCC_score
            input: 
                array of results,
                threshold of log ratio,
                threshold of theta
            output:
                tuple [threshold of log ratio, threshold of theta, threshold of array match, MCC score]
        preprocess
            input:
                array of results
            output:
                cumulative_true (array containing number of true reports beyond this threshold),
                cumulative_false (array containing number of true reports beyond this threshold),
                true_length (number of true reports),
                false_length (number of false reports)


thresholdcompiler.py
    contains 2 functions:
        compile_f1_score
            input:
                array storing best threshold for f1 score
                array of results,
                threshold of log ratio,
                threshold of theta
            output:
                best threshold array appended with tuple [threshold of log ratio, threshold of theta, threshold of array match, F1 score]
        compile_MCC_score
            input:
                array storing best threshold for MCC score
                array of results,
                threshold of log ratio,
                threshold of theta
            output:
                best threshold array appended with tuple [threshold of log ratio, threshold of theta, threshold of array match, MCC score]