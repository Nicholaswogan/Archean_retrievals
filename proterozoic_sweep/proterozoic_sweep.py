import numpy as np
import os
import time

import rfast

r = rfast.Rfast('inputs.scr')
r.initialize_retrieval("rpars.txt")

def bandpass_end(lam2, B):
    return lam2/(B + 1)

def get_filename(root_dir, O2, B, res, snr):
    file = ('O2=%.4e'%O2)+"_"('B=%.4f'%B)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

def spawn_retrieval(root_dir, O2, snr):
    res = 140
    B = 0.5
    # regrid + new snr
    lam1 = bandpass_end(1.0, B)
    
    lam_1 = np.array([0.5,0.6,lam1,1.0])
    res_1 = np.array([0,0,res])
    modes_1 = np.array([0,0,1],np.int32)
    snr0_1 = np.array([4,.1,snr])
    lam0_1 = np.array([0.84])
    r.wavelength_grid(lam_1, res_1, modes_1, snr0_1, lam0_1)
    
    file = "Proterozoic_O2="+'%.3e'%O2+".atm"
    r.scr.fnatm = file
    r.scr.fntmp = file

    # fake data
    F1, F2 = r.genspec_scr()
    dat, err = r.noise(F2)

    # filename
    file = get_filename(root_dir, O2, B, res, snr)

    # spawn retrievals
    r.nested_process(dat, err, file+'_all.pkl')

    r.remove_gas('o2')
    r.nested_process(dat, err, file+'_noO2.pkl')
    r.undo_remove_gas()

def spawn_all_retrievals(max_processes, root_dir, O2, snr):
    
    start = time.time()
    
    if not os.path.isdir(root_dir):
        raise Exception(root_dir+' must exist!')
    
    nt = len(O2)*2
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
        if ii < len(O2) and nr <= max_processes - 1:
            spawn_retrieval(root_dir, O2[ii], snr[ii])
            ii += 1
            
        finish = time.time()
        tot_time = (finish-start)/60
            
        fmt = "{:20}"
        print(fmt.format("running: "+'%i'%nr)+\
        fmt.format('completed: ''%i'%nc)+\
        fmt.format('total: ''%i'%nt)+\
        "{:30}".format('time: ''%.2f'%tot_time+' min'),end='\r')
        
        time.sleep(.1)
        
if __name__ == "__main__":
    
    root_dir = "results"
    max_processes = 48
    
    O2_1 = [1e-3, 5e-3, 1e-2, 2e-2]
    snr_1 = [10, 15, 20, 30, 40, 50]
    
    O2 = []
    snr = []
    for val in O2_1:
        for ss in snr_1:
            O2.append(val)
            snr.append(ss)
                    
    spawn_all_retrievals(max_processes, root_dir, O2, snr)
                
                
    
    
        
    

    
