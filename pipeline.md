## scripts and libraries
main.py
json
os
pandas
numpy
## delaunay from scipy.spatial
generatefeatures.py
functions.py
matcher.py
matcherfunc.py

## pipeline
1. load database
2. generate indirect features for all fingerprint
3. exhaustive matching over the entire database with iterating thresholds

## dependencies
1. fulfilled in main (import json)
2. main.py imports generatefeatures.py; generatefeatures.py imports functions.py
3. main.py imports matcher.py
   matcher.py imports matcherfunc.py