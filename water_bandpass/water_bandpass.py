import numpy as np
import os
import time

import rfast

r = rfast.Rfast('inputs.scr')
r.initialize_retrieval("rpars.txt")

def get_filename(root_dir, CH4, res, snr):
    file = ('CH4=%.4e'%CH4)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

def spawn_retrieval(root_dir, CH4, res, snr):
    # regrid + new snr
    lam_1 = np.array([0.816,0.98])
    res_1 = np.array([res])
    modes_1 = np.array([1],np.int32)
    snr0_1 = np.array([snr])
    lam0_1 = np.array([0.84])
    r.wavelength_grid(lam_1, res_1, modes_1, snr0_1, lam0_1)

    # set CH4
    ind = list(r.scr.species_r).index('ch4')
    r.scr.f0[ind] = CH4
    r.scr_genspec_inputs[0]= r.scr.f0

    # fake data
    F1, F2 = r.genspec_scr()
    dat, err = r.noise(F2)

    # filename
    file = get_filename(root_dir, CH4, res, snr)

    # spawn retrievals
    r.nested_process(dat, err, file+'_all.pkl')

    r.remove_gas('ch4')
    r.nested_process(dat, err, file+'_noCH4.pkl')
    r.undo_remove_gas()

    r.remove_gas('h2o')
    r.nested_process(dat, err, file+'_noH2O.pkl')
    r.undo_remove_gas()
    
def spawn_all_retrievals(max_processes, root_dir, CH4, res, snr):
    
    start = time.time()
    
    if not os.path.isdir(root_dir):
        raise Exception(root_dir+' must exist!')
    
    nt = len(CH4)*3
    ii = 0
    # while we still have models to run
    while ii < len(CH4):
        
        # check how many retrievals are running
        nr = 0
        nc = 0
        for process in r.retrieval_processes:
            if process['process'].is_alive():
                nr+=1
            else:
                nc+=1
    
        # if retrievals are less than max process,
        # then spawn 3 more
        if nr < max_processes - 3:
            spawn_retrieval(root_dir, CH4[ii], res[ii], snr[ii])
            ii += 1
            
        finish = time.time()
        tot_time = (finish-start)/60
            
        fmt = "{:20}"
        print(fmt.format("running: "+'%i'%nr)+\
        fmt.format('completed: ''%i'%nc)+\
        fmt.format('total: ''%i'%nt)+\
        "{:30}".format('time: ''%.2f'%tot_time+' min'),end='\r')
        
if __name__ == "__main__":
    
    root_dir = "results"
    max_processes = 48
    
    CH4_1 = [100.0e-6, 500.0e-6, 1000.0e-6, 5000.0e-6, 10000.0e-6]
    res_1 = [70, 140]
    snr_1 = [5, 10, 15, 20]

    CH4 = []
    snr = []
    res = []
    for val in CH4_1:
        for rr in res_1:
            for ss in snr_1:
                CH4.append(val)
                res.append(rr)
                snr.append(ss)
                        
    spawn_all_retrievals(max_processes, root_dir, CH4, res, snr)
                
                
    
    
        
    

    