import rfast
import numpy as np
import pickle
import time

r = rfast.Rfast('inputs.scr')

def get_filename(root_dir, B, res, snr):
    file = ('B=%.4f'%B)+"_"+('res=%.4f'%res)+"_"+('snr=%.4f'%snr)
    file = root_dir + "/" + file
    return file

def spawn_retrieval(rpars_file, root_dir, B, res, snr):
    
    r.initialize_retrieval(rpars_file)

    lam2 = 1
    lam1 = lam2/(B + 1)
    lam_1 = np.array([0.5,0.6,lam1,lam2])
    res_1 = np.array([0,0,res])
    modes_1 = np.array([0,0,1],np.int32)
    snr0_1 = np.array([4,.1,snr])
    lam0_1 = np.array([0.84])
    r.wavelength_grid(lam_1, res_1, modes_1, snr0_1, lam0_1)
    
    F1, F2 = r.genspec_scr()
    
    dat, err = r.noise_at_FpFs(F2, 3.55e-10)
    
    file = get_filename(root_dir, B, res, snr)
    
    sol = {}
    sol['lam'] = r.lam
    sol['dlam'] = r.dlam
    sol['dat'] = dat
    sol['err'] = err
    with open(file+'_data.pkl','wb') as fil:
        pickle.dump(sol, fil)

    # spawn retrievals
    r.nested_process(dat, err, file+'_all.pkl')
    
    r.remove_gas('h2o')
    r.nested_process(dat, err, file+'_noH2O.pkl')
    r.undo_remove_gas()
    
def gravity_known():
    rpars_file = "rpars_gravity_known.txt"
    root_dir = "gravity_known"
    B = 0.2
    res = 70
    snr = 10
    spawn_retrieval(rpars_file, root_dir, B, res, snr)
    
def gravity_unknown():
    rpars_file = "rpars_gravity_unknown.txt"
    root_dir = "gravity_unknown"
    B = 0.2
    res = 70
    snr = 10
    spawn_retrieval(rpars_file, root_dir, B, res, snr)
    
if __name__ == "__main__":
    gravity_known()
    gravity_unknown()
    while True:
        r.monitor_retrievals()
        print()
        time.sleep(10)
    
    