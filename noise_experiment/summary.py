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


sol = []


ii = 0
while True:
    try:
    
        tmp = {}

        file = "results_B=0.2_R=140_SNR=10/"+str(ii)
        print(file)

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
    except:
        break
    
    ii += 1
    
with open('summary.pkl','wb') as f:
    pickle.dump(sol,f)
