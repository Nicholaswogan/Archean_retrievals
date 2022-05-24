import numpy as np
import os
import time

import rfast

r = rfast.Rfast('inputs.scr')
r.initialize_retrieval("rpars.txt")

def bandpass_end(lam2, B):
    return lam2/(B + 1)

def get_filename(root_dir, B, res, snr):
    file = ('B=%.4f'%B)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

def spawn_retrieval(root_dir, B, res, snr, lam_end = 1.0, lam_begin = None, bandpass_from_end = True, FpFs_err = None):
    # regrid + new snr
    if bandpass_from_end:
        lam1 = bandpass_end(lam_end, B)
        lam_1 = np.array([0.5,0.6,lam1,lam_end])
    else
        lam2 = lam_begin*(1+B)
        lam_1 = np.array([0.5,0.6,lam_begin,lam2])
    
    lam_1 = np.array([0.5,0.6,lam1,1.0])
    res_1 = np.array([0,0,res])
    modes_1 = np.array([0,0,1],np.int32)
    snr0_1 = np.array([4,.1,snr])
    lam0_1 = np.array([0.84])
    r.wavelength_grid(lam_1, res_1, modes_1, snr0_1, lam0_1)

    # fake data
    F1, F2 = r.genspec_scr()
    if FpFs_err is None:
        dat, err = r.noise(F2)
    else:
        dat, err = r.noise_at_FpFs(F2, FpFs_err)

    # filename
    file = get_filename(root_dir, B, res, snr)

    # spawn retrievals
    r.nested_process(dat, err, file+'_all.pkl')

    r.remove_gas('o2')
    r.nested_process(dat, err, file+'_noO2.pkl')
    r.undo_remove_gas()

    r.remove_gas('h2o')
    r.nested_process(dat, err, file+'_noH2O.pkl')
    r.undo_remove_gas()
    
    r.remove_gas('o3')
    r.nested_process(dat, err, file+'_noO3.pkl')
    r.undo_remove_gas()
    
def spawn_all_retrievals(max_processes, root_dir, B, res, snr, **kwargs):
    
    start = time.time()
    
    if not os.path.isdir(root_dir):
        raise Exception(root_dir+' must exist!')
    
    nt = len(B)*4
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
                
        if nc == nt:
            break
    
        # if retrievals are less than max process,
        # then spawn 4 more
        if ii < len(B) and nr < max_processes - 4:
            spawn_retrieval(root_dir, B[ii], res[ii], snr[ii], **kwargs)
            ii += 1
            
        finish = time.time()
        tot_time = (finish-start)/60
            
        fmt = "{:20}"
        print(fmt.format("running: "+'%i'%nr)+\
        fmt.format('completed: ''%i'%nc)+\
        fmt.format('total: ''%i'%nt)+\
        "{:30}".format('time: ''%.2f'%tot_time+' min'),end='\r')
        
        time.sleep(.1)
        
def experiment_1():
    root_dir = "results"
    max_processes = 48
    
    B_1 = [0.2, 0.25, 0.3, 0.4, 0.5, 0.6]
    res_1 = [70, 140]
    snr_1 = [5, 10, 15, 20]
    
    B = []
    snr = []
    res = []
    for bb in B_1:
        for rr in res_1:
            for ss in snr_1:
                B.append(bb)
                res.append(rr)
                snr.append(ss)
                        
    spawn_all_retrievals(max_processes, root_dir, B, res, snr)
    
def experiment_2():
    root_dir = "results_experiment_2"
    max_processes = 48
    
    B_1 = [0.15, 0.2, 0.3, 0.4]
    res_1 = [70, 140]
    snr_1 = [5, 10, 15, 20]
    
    B = []
    snr = []
    res = []
    for bb in B_1:
        for rr in res_1:
            for ss in snr_1:
                B.append(bb)
                res.append(rr)
                snr.append(ss)
                        
    spawn_all_retrievals(max_processes, root_dir, B, res, snr, \
                        lam_end = None, lam_begin = 0.65, bandpass_from_end = False, FpFs_err = 3.55e-10)
        
if __name__ == "__main__":
    experiment_2()
    
    
                
                
    
    
        
    

    
