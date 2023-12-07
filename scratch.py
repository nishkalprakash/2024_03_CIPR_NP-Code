#%% Imports
from itertools import combinations

def nC2(imp_fea_dict):
        for fea_pair in combinations(imp_fea_dict.items(),2):
            yield dict(fea_pair)

def chain(arrs,func=nC2):
    for arr in arrs:
        if func is None:
            yield from arr
        else:
            yield from func(arr)
#%%
test_dict = {
    1:{
        (1,1):[[1,1],[1,1]],
        (1,2):[[1,2],[1,2]]
        },
    2:{
        (2,1):[[2,1],[2,1]],
        (2,2):[[2,2],[2,2]]
        },
}


#%%
# from pprint import pprint
# ll=list(chain(test_dict.values()))
# pprint(ll)

def get_imposter(test_dict,n_finger_per_person=1):
    # imp_fea_dict_values = test_dict
    for i in range(n_finger_per_person):
        imposter_dict = {}
        for value in test_dict.values():
            k,v=list(value.items())[i]
            imposter_dict[k]=v
        # imposter_dict = {}
        # for value in imp_fea_dict_values:
        yield imposter_dict
list(chain(get_imposter(test_dict,2)))
# %%
# [x.values() for x in ll]
# [x.keys() for x in ll]