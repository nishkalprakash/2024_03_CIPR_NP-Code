# import json
import pandas as pd
import generatefeatures as gf
import matcher as mc
import thresholdtester as tt
import numpy as np
from os import cpu_count

from multiprocessing.pool import Pool

# def parallel_compute(data):

#     a,b,fea = data
#     similarity_matrix = mc.match(fea, a, b)
#     f1_sc = tt.calculate_f1_score(similarity_matrix, a, b)
#     mcc_sc = tt.calculate_MCC_score(similarity_matrix, a, b)
#     return a,b,f1_sc, mcc_sc

def compute_eer(t1_t2_fea_dt_dst):
    t1, t2, fea, denom_type, dist_type = t1_t2_fea_dt_dst
    similarity_matrix = mc.match(fea, t1, t2, denom_type, dist_type)
    """
    @nishkalprakash
    call calculate_block_far_frr_score for 1%
    call calculate_grain_far_frr_score for 0.1%
    @abhibhuprakash
    call calculate_far_frr_score(gr=1) for 1%
    call calculate_far_frr_score(gr=0.1) for 0.1%
    """
    return tt.calculate_far_frr_score(similarity_matrix, t1, t2) # def gr = 0.1

def calc_eer(T1,T2,fea,denom_type='min', dist_type='euclidean_norm',debug=False):
    # far_score = []
    # frr_score = []
    out_file = Path(f"eer_T1[{T1[0]},{T1[1]},{T1[2]}]_T2[{T2[0]},{T2[1]},{T2[2]}]_{denom_type}_{dist_type}.csv")
    if out_file.exists():
        print(f"File {out_file} already exists. Skipping...")
        return
    else:
        print(f"Writing to file {out_file}")
        print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
    head= "T1,T2,T3,FAR,FRR,EER\n"
    with out_file.open('w') as f:
        f.write(head)

    def write_row(t1_t2_t3_far_frr_eer):
        t1,t2,t3, far, frr, eer = t1_t2_t3_far_frr_eer
        row = f"{t1:.3f},{t2:.3f},{t3:.0f},{far*100:.2f},{frr*100:.2f},{eer*100:0.2f}\n"
        print(row.replace(",","\t\t"),end="")
        with out_file.open('a') as f:
                f.write(row)

    if debug:
        # Run in single core
        print("Starting serial computation")
        print("Number of processors: ", 1)
        print(head.replace(",", "\t\t"))
        for t1_t2_fea_dt_dst in gen_t1_t2(T1,T2,fea,denom_type,dist_type):
            write_row(compute_eer(t1_t2_fea_dt_dst))
        
    else:
        # run in parallel cores
        with Pool(cpu_count()-1) as p:
            print("Starting parallel computation")
            print("Number of processors: ", cpu_count()-1)
            print(head.replace(",", "\t\t"))
            for t1_t2_t3_far_frr_eer in p.imap(compute_eer, gen_t1_t2(T1,T2,fea,denom_type, dist_type)):
                write_row(t1_t2_t3_far_frr_eer)

def gen_t1_t2(T1_range,T2_range,*args):
        threshold = (
            (i,j) for i in np.arange(*T1_range)
                  for j in np.arange(*T2_range)
        )
        
        for T1,T2 in threshold:
            yield T1, T2, *args

if __name__ == '__main__':
    from pathlib import Path
    json_files = [r'Datasets\anguli_10_100_fingernet.json']
    df = pd.read_json(json_files[0],orient='records')
    fea = gf.generatefeatures(df)
    T1_range = (0.1,2,0.1)
    T2_range = (0.01,0.13,0.01)
    # gr = 0.1
    denom_type = ['average', 'geometric', 'harmonic', 'min']
    dist_type = ['euclidean_norm','euclidian_log_norm']
    # TODO: add these dist measures as well ['manhattan', 'cosine', 'minkowski']
    debug = True
    # debug = False

    for dt in denom_type:
        for dst in dist_type:
            if (dt,dst) == ('harmonic','euclidean_norm'):
                continue
            calc_eer(T1_range,T2_range,fea,dt,dst)
             
    # calc_eer(T1_range,T2_range,fea,denom_type[2], dist_type[0],debug)
