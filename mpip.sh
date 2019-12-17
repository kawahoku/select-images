echo "test begin"
conda create -n test python=3.6
conda activate test
echo "\"test\" env activated"
echo "install https://github.com/kawahoku/select-images..."
python -m pip install git+https://github.com/kawahoku/select-images
echo "Done."
