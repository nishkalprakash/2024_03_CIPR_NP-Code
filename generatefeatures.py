# generates indirect feature vectors for all fingerprint in the dataframe

import pandas as pd
from scipy.spatial import Delaunay
import functions as fn

def generatefeatures(df):

    # fetch name of fingerprint for current index and return it
    def get_name(index):
        name = df['path'][index]
        name = name.replace('/', '_')
        name = name.replace('.tif', '')
        return name
    
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
        name = get_name(i)
        fingerprint = fetch_fingerprint(i)
        points, minutiae = generate_minutiae(fingerprint)
        triangles = triangulate(points, minutiae)
        features_array = fn.ret_arr(triangles)
        db_array.append([name, features_array])

    return db_array
    