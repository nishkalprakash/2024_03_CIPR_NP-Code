# import json
import pandas as pd
import generatefeatures as gf
import matcher as mc
import thresholdtester as tt
import numpy as np
from os import cpu_count

from multiprocessing.pool import Pool

def parallel_compute(data):

    a,b,fea = data
    similarity_matrix = mc.match(fea, a, b)
    f1_sc = tt.calculate_f1_score(similarity_matrix, a, b)
    mcc_sc = tt.calculate_MCC_score(similarity_matrix, a, b)
    return a,b,f1_sc, mcc_sc
def parallel_compute_eer(data):

    a,b,fea = data
    similarity_matrix = mc.match(fea, a, b)
    far_sc = tt.calculate_far(similarity_matrix, a, b)
    frr_sc = tt.calculate_frr(similarity_matrix, a, b)
    return a,b,far_sc, frr_sc, (frr_sc[3] + far_sc[3])/2



def calc_f1(T1,T2,fea):
    f1_score = []
    mcc_score = []
    out_file = Path(f"output_f1_T1[{T1[0]:0.2f},{T1[1]:0.2f},{T1[2]:0.2f}]_T2[{T2[0]:0.3f},{T2[1]:0.3f},{T1[2]:0.3f}].csv")
    with Pool(cpu_count()-1) as p:
        # start = time.time()
        print("Starting parallel computation")
        print("Number of processors: ", cpu_count()-1)
        # head= "T1,T2,f1_T,FAR,mcc_T,FRR,EER\n"
        head= "T1,T2,F1_T,F1,MCC_T,MCC\n"
        print(head.replace(",", "\t\t"))
        with out_file.open('a') as f:
            f.write(head)
        for t1,t2,f1_sc, mcc_sc in p.imap_unordered(parallel_compute, gen(T1,T2,fea),10):
            f1_score.append(f1_sc)
            mcc_score.append(mcc_sc)
            # row = f"{t1:.2f},{t2:.2f},{f1_sc[2]:.0f},{f1_sc[3]*100:.2f},{mcc_sc[2]:.0f},{mcc_sc[3]*100:.2f},{eer*100:0.2f}\n"
            row = f"{t1:.2f},{t2:.3f},{f1_sc[2]:.0f},{f1_sc[3]*100:.2f},{mcc_sc[2]:.0f},{mcc_sc[3]*100:.2f}\n"
            print(row.replace(",","\t\t"),end="")
            with out_file.open('a') as f:
                f.write(row)

def calc_eer(T1,T2,fea):
    far_score = []
    frr_score = []
    out_file = Path(f"output_eer_T1[{T1[0]:0.2f},{T1[1]:0.2f},{T1[2]:0.2f}]_T2[{T2[0]:0.3f},{T2[1]:0.3f},{T1[2]:0.3f}].csv")
    with Pool(cpu_count()-1) as p:
        print("Starting parallel computation")
        print("Number of processors: ", cpu_count()-1)
        head= "T1,T2,FAR_T,FAR,FRR_T,FRR,EER\n"
        print(head.replace(",", "\t\t"))
        with out_file.open('a') as f:
            f.write(head)
        for t1,t2,far_sc, frr_sc, eer in p.imap_unordered(parallel_compute_eer, gen(T1,T2,fea),10):
            far_score.append(far_sc)
            frr_score.append(frr_sc)
            row = f"{t1:.2f},{t2:.2f},{far_sc[2]:.0f},{far_sc[3]*100:.2f},{frr_sc[2]:.0f},{frr_sc[3]*100:.2f},{eer*100:0.2f}\n"
            print(row.replace(",","\t\t"),end="")
            with out_file.open('a') as f:
                f.write(row)

def gen(T1,T2,fea):
        threshold = (
            (i,j) for i in np.arange(*T1)
                  for j in np.arange(*T2)
        )
        
        for a,b in threshold:
            yield a, b, fea

if __name__ == '__main__':
    from pathlib import Path
    json_files = [r'Datasets\anguli_10_100_fingernet.json']
    df = pd.read_json(json_files[0],orient='records')
    fea = gf.generatefeatures(df)
    T1 = (0.0,1.0,0.1)
    T2 = (0.0,1.0,0.1)
    # calc_f1(T1,T2,fea)
    calc_eer(T1,T2,fea)
