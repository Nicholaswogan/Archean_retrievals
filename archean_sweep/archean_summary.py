import numpy as np
import pickle
from rfast import detection_sigma

def get_filename(root_dir, B, CH4, res, snr):
    file = ('B=%.4f'%B)+"_"+('CH4=%.4e'%CH4)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

root_dir = "results"
B_1 = [0.2, 0.25, 0.3, 0.4, 0.5]
CH4_1 = [500.0e-6, 1000.0e-6, 5000.0e-6, 10000.0e-6]
res_1 = [70, 140]
snr_1 = [5, 10, 15, 20]

sol = {}

for bb in B_1:
    sol[bb] = {}
    for val in CH4_1:
        sol[bb][val] = {}
        for rr in res_1:
            sol[bb][val][rr] = {}
            for ss in snr_1:
                file = get_filename(root_dir, bb, val, rr, ss)
                
                sol[bb][val][rr][ss] = {}
                sol[bb][val][rr][ss]['evidence'] = {}
                with open(file+'_all.pkl','rb') as f:
                    results = pickle.load(f)
                
                all_evidence = results['logz'][-1]
                sol[bb][val][rr][ss]['evidence']['all'] = all_evidence

                with open(file+'_noCH4.pkl','rb') as f:
                    results = pickle.load(f)

                CH4_evidence = results['logz'][-1]
                sol[bb][val][rr][ss]['evidence']['CH4'] = CH4_evidence


                with open(file+'_noH2O.pkl','rb') as f:
                    results = pickle.load(f)

                H2O_evidence = results['logz'][-1]
                sol[bb][val][rr][ss]['evidence']['H2O'] = H2O_evidence

                lnB_H2O = all_evidence - H2O_evidence
                lnB_CH4 = all_evidence - CH4_evidence
                
                sol[bb][val][rr][ss]['sig_CH4'] = detection_sigma(lnB_CH4)
                sol[bb][val][rr][ss]['sig_H2O'] = detection_sigma(lnB_H2O)
                

with open('archean_summary.pkl','wb') as f:
    pickle.dump(sol,f)


