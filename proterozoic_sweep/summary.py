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


def get_filename(root_dir, O2, B, res, snr):
    file = ('O2=%.4e'%O2)+"_"+('B=%.4f'%B)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

root_dir = "results"
max_processes = 48

O2_1 = [1e-3, 5e-3, 1e-2, 2e-2]
snr_1 = [10, 15, 20, 30, 40, 50]

res = 140
B = 0.5

sol = {}

for val in O2_1:
    sol[val] = {}
    for ss in snr_1:
        try:
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
            
        except:
            print(file)
            pass
                

with open('summary.pkl','wb') as f:
    pickle.dump(sol,f)
