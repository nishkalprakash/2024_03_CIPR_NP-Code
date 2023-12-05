# import json
import pandas as pd
import generatefeatures as gf
import matcher as mc
import thresholdtester as tt
import numpy as np

json_files = [r'Datasets\anguli_10_100_fingernet.json']
df = pd.read_json(json_files[0],orient='records')

new_df = gf.pair_selector(df, 3)