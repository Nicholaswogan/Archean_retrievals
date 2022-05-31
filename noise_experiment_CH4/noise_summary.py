import numpy as np
import pickle
from rfast import detection_sigma

def write_summary(root_dir, outfile):

    sol = []
    ii = 0
    
    while True:
        try:
            tmp = {}

            file = root_dir+"/"+str(ii)

            with open(file+'_all.pkl','rb') as f:
                results = pickle.load(f)
            all_evidence = results['logz'][-1]
            tmp['evidence_all'] = all_evidence

            with open(file+'_noCH4.pkl','rb') as f:
                results = pickle.load(f)
            CH4_evidence = results['logz'][-1]
            tmp['evidence_CH4'] = CH4_evidence
            lnB_CH4 = all_evidence - CH4_evidence

            tmp['sig_CH4'] = detection_sigma(lnB_CH4)
            
            print(ii)
                
            sol.append(tmp)
        except FileNotFoundError:
            break
        
        ii += 1 
        
    with open(outfile,'wb') as f:
        pickle.dump(sol,f)
        
if __name__ == "__main__":
    outfile = "noise_summary_B=0.2_R=70_SNR=5.pkl"
    root_dir = "results_B=0.2_R=70_SNR=5"
    write_summary(root_dir, outfile)
