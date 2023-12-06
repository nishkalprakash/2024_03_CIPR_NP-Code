# generates indirect feature vectors for all fingerprint in the dataframe

import pandas as pd
from scipy.spatial import Delaunay
import functions as fn
import random as rn
import numpy as np

def get_name(index, df):
    name = df['path'][index]
    name = name.replace('/', '_')
    name = name.replace('.tif', '')
    return name

def generatefeatures(df):

    # fetch name of fingerprint for current index and return it
    # fetch fingerprint for current index and return it
    def fetch_fingerprint(index):
        fingerprint = []
        fingerprint.append(pd.DataFrame(df['mv'][index], columns=['x', 'y', 'value']))
        return fingerprint

    # generate minutiae from fingerprint and return points and minutiae
    def generate_minutiae(fingerprint):
        points = []
        minutiae = []
        for i in range(len(fingerprint[0])):
            points.append([fingerprint[0]['x'][i], fingerprint[0]['y'][i]])
            minutiae.append([fingerprint[0]['x'][i], fingerprint[0]['y'][i], fingerprint[0]['value'][i]])
        return points, minutiae

    # perform delaunay triangulation and return triangles
    def triangulate(points, minutiae):
        tri = Delaunay(points)

        triangles = []
        for i in range(len(tri.simplices)):
            triangles.append([minutiae[tri.simplices[i][0]], minutiae[tri.simplices[i][1]], minutiae[tri.simplices[i][2]]])
        return triangles
    
    # store entire database into a single array
    db_array = []

    # generate indirect features for all triangles
    for i in range(len(df)):
        name = get_name(i, df)
        fingerprint = fetch_fingerprint(i)
        points, minutiae = generate_minutiae(fingerprint)
        triangles = triangulate(points, minutiae)
        features_array = fn.ret_arr(triangles)
        db_array.append([name, features_array])

    return db_array    

# check if input strings are similar:


def pair_selector(db, seed_count = 0):
    if seed_count == 0:
        return None
    
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
    
    impression_count = 0
    while True:
        x = get_name(0, db)
        y = get_name(impression_count, db)
        if check_name(x, y):
            impression_count += 1
        else:
            break
    
    fingerprint_count = len(db) / impression_count

    # generate a tuple of random integers less than impression_count. size of tuple is seed_count
    # if impression_count is less than seed count, return every integer in range(impression_count)

    index_tuple = []
    if seed_count >= impression_count:
        for i in range(impression_count):
            index_tuple.append(i)
    else:
        # use numpy to pick 3 numbers from 10 numbers without replacement
        index_tuple = np.random.choice(impression_count - 1, seed_count, replace=False)
        # i = rn.randint(0, impression_count - 1)
        # index_tuple.append(i)
        # while True:
        #     # generate a random interger
        #     i = rn.randint(0, impression_count - 1)
        #     # check if i already lies in index_tuple array
        #     for j in index_tuple:
        #         if i == j:
        #             continue
        #         else:
        #             index_tuple.append(i)
        #             continue
        #     if len(index_tuple) == seed_count:
        #         break
    index_tuple.sort()
    
    # from the df, select impressions indexed index_tuple for each fingerprint
    new_db = []
    for i in range(fingerprint_count):
        for j in index_tuple:
            new_db.append(db[i * impression_count + j])

    return new_db