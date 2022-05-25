import numpy as np
import pickle
from rfast import detection_sigma

def get_filename(root_dir, B, res, snr):
    file = ('B=%.4f'%B)+""+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

def write_summary(root_dir, outfile, B_1, res_1, snr_1):

    sol = {}

    for bb in B_1:
        sol[bb] = {}
        for rr in res_1:
            sol[bb][rr] = {}
            for ss in snr_1:
                file = get_filename(root_dir, bb, rr, ss)

                sol[bb][rr][ss] = {}
                sol[bb][rr][ss]['evidence'] = {}
                with open(file+'_all.pkl','rb') as f:
                    results = pickle.load(f)
                all_evidence = results['logz'][-1]
                sol[bb][rr][ss]['evidence']['all'] = all_evidence
                
                with open(file+'_noO2.pkl','rb') as f:
                    results = pickle.load(f)
                O2_evidence = results['logz'][-1]
                sol[bb][rr][ss]['evidence']['O2'] = O2_evidence
                lnB_O2 = all_evidence - O2_evidence
                sol[bb][rr][ss]['sig_O2'] = detection_sigma(lnB_O2)

                with open(file+'_noH2O.pkl','rb') as f:
                    results = pickle.load(f)
                H2O_evidence = results['logz'][-1]
                sol[bb][rr][ss]['evidence']['H2O'] = H2O_evidence
                lnB_H2O = all_evidence - H2O_evidence
                sol[bb][rr][ss]['sig_H2O'] = detection_sigma(lnB_H2O)
                
                # make O3 optional
                try:
                    with open(file+'_noO3.pkl','rb') as f:
                        results = pickle.load(f)
                    O3_evidence = results['logz'][-1]
                    sol[bb][rr][ss]['evidence']['H2O'] = O3_evidence
                    lnB_O3 = all_evidence - O3_evidence
                    sol[bb][rr][ss]['sig_O3'] = detection_sigma(lnB_O3)
                except:
                    pass

    with open(outfile,'wb') as f:
        pickle.dump(sol,f)
        
def summary_experiment_1():
    root_dir = "results"
    outfile = "modern_summary.pkl"
    B_1 = [0.2, 0.25, 0.3, 0.4, 0.5, 0.6]
    res_1 = [70, 140]
    snr_1 = [5, 10, 15, 20]
    write_summary(root_dir, outfile, B_1, res_1, snr_1)
    
# experiment 2
def summary_experiment_2():
    root_dir = "results_experiment_2"
    outfile = "modern_summary_experiment_2.pkl"
    B_1 = [0.15, 0.2, 0.3, 0.4]
    res_1 = [70, 140]
    snr_1 = [5, 10, 15, 20]
    write_summary(root_dir, outfile, B_1, res_1, snr_1)
    
if __name__ == "__main__":
    summary_experiment_2()
