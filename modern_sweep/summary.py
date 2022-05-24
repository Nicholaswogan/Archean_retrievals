import pickle
import numpy as np

from scipy import optimize
from scipy import special
from scipy import stats
import scipy as sp

def rho(sigma):
    return 1 - special.erf(sigma/np.sqrt(2))

def bayes_factor(sigma):
    r = rho(sigma)
    return - 1/(np.exp(1)*r*np.log(r))

def objective(x, bayes_factor_input):
    sigma = x[0]
    return bayes_factor(sigma) - bayes_factor_input

def sigma_significance(bayes_factor_input):
    if bayes_factor_input > 1e8:
        warnings.warn("Bayes factors larger than 1e8 can not be computed. Returning sigma = 6.392455915996625")
        return 6.392455915996625
    if bayes_factor_input <= 1:
#         warnings.warn("ahhhh")
        return 0.9004526284839545
    initial_cond = np.array([6.0])
    sol = optimize.root(objective, initial_cond, args = (bayes_factor_input,))
    if not sol.success:
        raise Exception("Root solving failed: "+sol.message)
    return sol.x[0]

def detection_sigma(lnB):
    if lnB < np.log(2e1):
        return sigma_significance(np.exp(lnB))
    
    logp = np.arange(-100.00,-0.00,.01) #reverse order
    logp = logp[::-1] # original order
    P = 10.0**logp
    Barr = -1./(np.exp(1)*P*np.log(P))

    sigma = np.arange(0.1,100.10,.01)
    p_p = sp.special.erfc(sigma/np.sqrt(2.0))

    B = np.exp(lnB)
    pvalue = 10.0**np.interp(np.log10(B),np.log10(Barr),np.log10(P))
    sig = np.interp(pvalue,p_p[::-1],sigma[::-1])

    return sig


def get_filename(root_dir, B, res, snr):
    file = ('B=%.4f'%B)+""+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

root_dir = "results"
max_processes = 48

B_1 = [0.2, 0.25, 0.3, 0.4, 0.5, 0.6]
res_1 = [70, 140]
snr_1 = [5, 10, 15, 20]

sol = {}

for bb in B_1:
    sol[bb] = {}
    for rr in res_1:
        sol[bb][rr] = {}
        for ss in snr_1:
            
            print('hi')
            try:
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


                with open(file+'_noH2O.pkl','rb') as f:
                    results = pickle.load(f)

                H2O_evidence = results['logz'][-1]
                sol[bb][rr][ss]['evidence']['H2O'] = H2O_evidence

                with open(file+'_noO3.pkl','rb') as f:
                    results = pickle.load(f)

                O3_evidence = results['logz'][-1]
                sol[bb][rr][ss]['evidence']['H2O'] = O3_evidence

                lnB_H2O = all_evidence - H2O_evidence
                lnB_O2 = all_evidence - O2_evidence
                lnB_O3 = all_evidence - O3_evidence

                sol[bb][rr][ss]['sig_O2'] = detection_sigma(lnB_O2)
                sol[bb][rr][ss]['sig_H2O'] = detection_sigma(lnB_H2O)
                sol[bb][rr][ss]['sig_O3'] = detection_sigma(lnB_O3)
            except:
                pass
                

with open('summary.pkl','wb') as f:
    pickle.dump(sol,f)
