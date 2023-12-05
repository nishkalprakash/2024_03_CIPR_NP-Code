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

def parallel_compute_eer(t1_t2_fea_gr):
    t1, t2, fea, gr = t1_t2_fea_gr
    similarity_matrix = mc.match(fea, t1, t2)
    """
    @nishkalprakash
    call calculate_block_far_frr_score for 1%
    call calculate_grain_far_frr_score for 0.1%
    @abhibhuprakash
    call calculate_far_frr_score(gr=1) for 1%
    call calculate_far_frr_score(gr=0.1) for 0.1%
    """
    return tt.calculate_far_frr_score(similarity_matrix, t1, t2, gr) # gr = 1 | 0.1



def calc_f1(T1,T2,fea):
    f1_score = []
    mcc_score = []
    out_file = Path(f"output_f1_T1[{T1[0]:0.2f},{T1[1]:0.2f},{T1[2]:0.2f}]_T2[{T2[0]:0.3f},{T2[1]:0.3f},{T1[2]:0.3f}].csv")
    with Pool(cpu_count()-1) as p:
        # start = time.time()
        print("Starting parallel computation")
        print("Number of processors: ", cpu_count()-1)
        head= "T1,T2,F1_T,F1,MCC_T,MCC\n"
        print(head.replace(",", "\t\t"))
        with out_file.open('a') as f:
            f.write(head)
        for t1,t2,f1_sc, mcc_sc in p.imap_unordered(parallel_compute, gen(T1,T2,fea),10):
            f1_score.append(f1_sc)
            mcc_score.append(mcc_sc)
            row = f"{t1:.2f},{t2:.3f},{f1_sc[2]:.0f},{f1_sc[3]*100:.2f},{mcc_sc[2]:.0f},{mcc_sc[3]*100:.2f}\n"
            print(row.replace(",","\t\t"),end="")
            with out_file.open('a') as f:
                f.write(row)

def calc_eer(T1,T2,fea,gr=1,debug=False):
    # far_score = []
    # frr_score = []
    out_file = Path(f"output_eer_T1[{T1[0]:0.3f},{T1[1]:0.3f},{T1[2]:0.3f}]_T2[{T2[0]:0.3f},{T2[1]:0.3f},{T1[2]:0.3f}].csv")
    
    head= "T1,T2,T3,FAR,FRR,EER\n"
    with out_file.open('w') as f:
        f.write(head)

    def write_row(t1_t2_t3_far_frr_eer):
        t1,t2,t3, far, frr, eer = t1_t2_t3_far_frr_eer
        row = f"{t1:.2f},{t2:.2f},{t3:.0f},{far*100:.2f},{frr*100:.2f},{eer*100:0.2f}\n"
        print(row.replace(",","\t\t"),end="")
        with out_file.open('a') as f:
                f.write(row)

    if debug:
        # Run in single core
        print("Starting serial computation")
        print("Number of processors: ", 1)
        print(head.replace(",", "\t\t"))
        for t1_t2_fea_gr in gen(T1,T2,fea,gr):
            write_row(parallel_compute_eer(t1_t2_fea_gr))
        
    else:
        # run in parallel cores
        with Pool(cpu_count()-1) as p:
            print("Starting parallel computation")
            print("Number of processors: ", cpu_count()-1)
            print(head.replace(",", "\t\t"))
            for t1_t2_t3_far_frr_eer in p.imap(parallel_compute_eer, gen(T1,T2,fea,gr)):
                write_row(t1_t2_t3_far_frr_eer)

def gen(T1_range,T2_range,fea,gr=1):
        threshold = (
            (i,j) for i in np.arange(*T1_range)
                  for j in np.arange(*T2_range)
        )
        
        for T1,T2 in threshold:
            yield T1, T2, fea, gr

if __name__ == '__main__':
    from pathlib import Path
    json_files = [r'Datasets\anguli_10_100_fingernet.json']
    df = pd.read_json(json_files[0],orient='records')
    fea = gf.generatefeatures(df)
    T1_range = (0.1,1,0.1)
    T2_range = (0.01,0.2,0.01)
    # calc_f1(T1,T2,fea)
    gr = 0.1
    calc_eer(T1_range,T2_range,fea,gr,debug=False)
