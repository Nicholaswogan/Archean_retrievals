
```sh
# create conda environment
conda create -n rfast -c conda-forge python numpy numba scipy ruamel.yaml astropy emcee dynesty multiprocess scikit-build

# activate
conda activate rfast

# rfast
git clone https://github.com/Nicholaswogan/rfast.git
cd rfast
git checkout 20821d0a9462457a51a59f1e265739cfd5d9427c
python -m pip install --no-deps --no-build-isolation . -v
cd ..
rm -rf rfast
```