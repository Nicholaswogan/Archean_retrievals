import numpy as np
import pickle
from rfast import detection_sigma

def get_filename(root_dir, O2, B, res, snr):
    file = ('O2=%.4e'%O2)+"_"+('B=%.4f'%B)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

root_dir = "results"

O2_1 = [1e-3, 5e-3, 1e-2, 2e-2]
snr_1 = [10, 15, 20, 30, 40, 50]

res = 140
B = 0.5

sol = {}

for val in O2_1:
    sol[val] = {}
    for ss in snr_1:
        file = get_filename(root_dir, val, B, res, ss)
        
        sol[val][ss] = {}
        sol[val][ss]['evidence'] = {}
        with open(file+'_all.pkl','rb') as f:
            results = pickle.load(f)

        all_evidence = results['logz'][-1]
        sol[val][ss]['evidence']['all'] = all_evidence

        with open(file+'_noO2.pkl','rb') as f:
            results = pickle.load(f)

        O2_evidence = results['logz'][-1]
        sol[val][ss]['evidence']['O2'] = O2_evidence

        lnB_O2 = all_evidence - O2_evidence

        sol[val][ss]['sig_O2'] = detection_sigma(lnB_O2)
                

with open('proterozoic_summary.pkl','wb') as f:
    pickle.dump(sol,f)
