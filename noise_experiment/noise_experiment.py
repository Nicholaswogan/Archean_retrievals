import numpy as np
import os
import time

import rfast

r = rfast.Rfast('inputs.scr')
r.initialize_retrieval("rpars.txt")

def spawn_retrieval(root_dir, F2, iter):

    # fake data
    dat, err = r.noise(F2)

    # filename
    file = str(iter)

    # spawn retrievals
    r.nested_process(dat, err, file+'_all.pkl')
    
    r.remove_gas('h2o')
    r.nested_process(dat, err, file+'_noH2O.pkl')
    r.undo_remove_gas()
    
def spawn_all_retrievals(max_processes, root_dir, nt):
    
    F1, F2 = r.genspec_scr()
    
    start = time.time()
    
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
                
        if nc == nt:
            break
    
        # if retrievals are less than max process,
        # then spawn 3 more
        if ii < len(CH4) and nr < max_processes - 2:
            spawn_retrieval(root_dir, F2, ii)
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
    nt = 250
                        
    spawn_all_retrievals(max_processes, root_dir, nt)
                
                
    
    
        
    

    
