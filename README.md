
```sh
# create conda environment
conda create -n rfast -c conda-forge python numpy numba scipy ruamel.yaml astropy emcee dynesty multiprocess scikit-build

# activate
conda activate rfast

# rfast
git clone https://github.com/Nicholaswogan/rfast.git
cd rfast
git checkout 8064b821710e0fc49a4e2128625b5ed22ad28e8a
python -m pip install --no-deps --no-build-isolation . -v
cd ..
rm -rf rfast
```