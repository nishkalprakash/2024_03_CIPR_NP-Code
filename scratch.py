#%% Imports
from itertools import combinations

#%% 
def nC2(arr):
    for pair in combinations(arr,2):
        yield pair

def chain(arr_arr):
    for arr in arr_arr:
        yield from nC2(arr)
#%%
test_dict = {
    1:range(4),
    2:range(5,9),
    3:range(10,14)
}


#%%
list(chain(test_dict.values()))