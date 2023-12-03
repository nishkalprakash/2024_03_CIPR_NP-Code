# import json
import pandas as pd
import generatefeatures as gf
import matcher as mc
import thresholdtester as tt
# import numpy as np
from os import cpu_count

from multiprocessing.pool import Pool

def parallel_compute(data):

    a,b,fea = data
    # b = threshold[100 * i + j][1]
    similarity_matrix = mc.match(fea, a, b)
    f1_sc = tt.calculate_f1_score(similarity_matrix, a, b)
    mcc_sc = tt.calculate_MCC_score(similarity_matrix, a, b)
    return a,b,f1_sc, mcc_sc
    # f1_score.append(f1_sc)
    # mcc_score.append(mcc_sc)


if __name__ == '__main__':
    from pathlib import Path
    json_files = ['Datasets/FVC2002_DB1_A_fingernet.json']
    df = pd.read_json(json_files[0],orient='records')
    fea = gf.generatefeatures(df)
    threshold = zip(np.arange(0.1,1.3,0.01),np.arange(0.04,0.13,0.01))
    
    # for i in range(1,3,0.01):
    #     for j in range(5,16):
    #         threshold.append([i/100+1, j/100])
    # define arrays to store f1_score and mcc_score
    f1_score = []
    mcc_score = []

    def gen():
        # for i in range(100):
            # for j in range(100):
        for a,b in threshold:
                # a = threshold[100 * i + j][0]
                # b = threshold[100 * i + j][1]
            yield a, b, fea

    out_file = Path("output_t1[1-3]_t2[0-0.2].csv")
    with Pool(cpu_count()-1) as p:
        # start = time.time()
        print("Starting parallel computation")
        print("Number of processors: ", cpu_count()-1)
        head= "T1,T2,F1_T,F1,MCC_T,MCC\n"
        print(head.replace(",", "\t\t"))
        with out_file.open('a') as f:
            f.write(head)
        for t1,t2,f1_sc, mcc_sc in p.imap_unordered(parallel_compute, gen(),10):
            #  = x
            f1_score.append(f1_sc)
            mcc_score.append(mcc_sc)
            row = f"{t1:.2f},{t2:.2f},{f1_sc[2]:.0f},{f1_sc[3]*100:.2f},{mcc_sc[2]:.0f},{mcc_sc[3]*100:.2f}\n"
            print(row.replace(",","\t\t"),end="")
            with out_file.open('a') as f:
                f.write(row)
        
# loop over all threshold values
# also print threshold values and iteration number in a table format
    # print("Threshold 1 \t Threshold 2 \t Iteration")
    # for i in range(100):
        # for j in range(100):
            
            # print threshold values and iteration number in a table format
            # print("{0:.2f}".format(a), ",", "{0:.2f}".format(b), "\t\t", 100 * i + j)