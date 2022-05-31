import numpy as np
import os
import time
import pickle

import rfast

np.random.seed(0)

r = rfast.Rfast('inputs.scr')
r.initialize_retrieval("rpars.txt")

def spawn_retrieval(root_dir, F2, FpFs_err, iter):
    
    # filename
    file = root_dir+'/'+str(iter)

    # fake data
    dat, err = r.noise_at_FpFs(F2, FpFs_err)
    # save the data
    sol = {}
    sol['lam'] = r.lam
    sol['dlam'] = r.dlam
    sol['dat'] = dat
    sol['err'] = err
    with open(file+'_data.pkl','wb') as fil:
        pickle.dump(sol, fil)

    # spawn retrievals
    r.nested_process(dat, err, file+'_all.pkl')
    
    r.remove_gas('ch4')
    r.nested_process(dat, err, file+'_noCH4.pkl')
    r.undo_remove_gas()
    
def spawn_all_retrievals(max_processes, root_dir, nt, B, R, SNR, CH4, FpFs_err):
    lam2 = 1
    lam1 = lam2/(B + 1)
    lam = np.array([0.5,0.6,lam1,lam2])
    res = np.array([0,0,R])
    modes = np.array([0,0,1],np.int32)
    snr0 = np.array([4,.1,SNR])
    lam0 = np.array([0.84])
    r.wavelength_grid(lam, res, modes, snr0, lam0)
    
    # set CH4
    ind = list(r.scr.species_r).index('ch4')
    r.scr.f0[ind] = CH4
    r.scr_genspec_inputs[0]= r.scr.f0
    
    F1, F2 = r.genspec_scr()
    start = time.time()
    
    ntt = nt*2
    
    if not os.path.isdir(root_dir):
        raise Exception(root_dir+' must exist!')
    
    ii = 0
    # while we still have models to run
    while True:
        
        # check how many retrievals are running
        nr = 0
        nc = 0
        for process in r.retrieval_processes:
            if process['process'].is_alive():
                nr+=1
            else:
                nc+=1
                
        if nc == ntt:
            break
    
        # if retrievals are less than max process,
        # then spawn 2 more
        if nr <= max_processes - 2 and nr+nc <= ntt+2:
            spawn_retrieval(root_dir, F2, FpFs_err, ii)
            ii += 1
            
        finish = time.time()
        tot_time = (finish-start)/60
            
        fmt = "{:20}"
        print(fmt.format("running: "+'%i'%nr)+\
        fmt.format('completed: ''%i'%nc)+\
        fmt.format('total: ''%i'%ntt)+\
        "{:30}".format('time: ''%.2f'%tot_time+' min'),end='\r')
        
        time.sleep(1)
        
        
if __name__ == "__main__":
    
    root_dir = "results_B=0.2_R=140_SNR=5"
    max_processes = 40
    nt = 100
    R = 140
    B = 0.2
    
    SNR = 5
    CH4 = 500.0e-6
    
    FpFs_err = 3.55e-10
                        
    spawn_all_retrievals(max_processes, root_dir, nt, B, R, SNR, CH4, FpFs_err)
                
                
    
    
        
    

    
