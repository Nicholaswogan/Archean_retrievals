
```sh
# create conda environment
conda create -n rfast -c conda-forge python numpy numba scipy ruamel.yaml astropy emcee dynesty multiprocess scikit-build

# activate
conda activate rfast

# rfast
git clone https://github.com/Nicholaswogan/rfast.git
cd rfast
git checkout b3b4fca02f75d2c8acf0eb7913af8e9e1db9eeb1
python -m pip install --no-deps --no-build-isolation . -v
cd ..
rm -rf rfast
```