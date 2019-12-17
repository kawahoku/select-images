echo""
echo "test begin"
echo""
conda create -n test python=3.6
conda activate test
echo""
echo "\"test\" env activated"
echo""
echo "install https://github.com/kawahoku/select-images..."
echo""
python -m pip install git+https://github.com/kawahoku/select-images
echo "Done."
echo""
