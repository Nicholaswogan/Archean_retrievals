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

            with open(file+'_noH2O.pkl','rb') as f:
                results = pickle.load(f)
            H2O_evidence = results['logz'][-1]
            tmp['evidence_H2O'] = H2O_evidence
            lnB_H2O = all_evidence - H2O_evidence

            tmp['sig_H2O'] = detection_sigma(lnB_H2O)
            
            print(ii)
                
            sol.append(tmp)
        except FileNotFoundError:
            break
        
        ii += 1 
        
    with open(outfile,'wb') as f:
        pickle.dump(sol,f)
        
if __name__ == "__main__":
    outfile = "noise_summary_B=0.2_R=70_SNR=5_noH2O.pkl"
    root_dir = "results_B=0.2_R=70_SNR=5_noH2O"
    write_summary(root_dir, outfile)
