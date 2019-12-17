if [ $# -ne 1 ]; then
    echo "You must specify the installation directory!"
    exit 1
fi


case $1 in
    /*) PLUGIN_DIR=$1;;
    *) PLUGIN_DIR=$PWD/$1;;
esac

INSTALL_DIR="${PLUGIN_DIR}/SelectImages"

echo "Install to \"$INSTALL_DIR\"..."
if [ -e "$INSTALL_DIR" ]; then
    echo "\"$INSTALL_DIR\" already exists!"
fi

echo ""

type git || {
    echo 'Please install git or update your path to include the git executable!'
    exit 1
}
echo ""

git=$(which git)

if ! [ -e "$INSTALL_DIR" ]; then
    echo "Begin cloning Select_image_gui..."
    mkdir -p "$PLUGIN_DIR"
    $git clone https://github.com/kawahoku/select-images "$INSTALL_DIR"
    echo "Done."
    echo ""
fi

python=$(which python)
python_version=$("$python" --version)
pip=$(which pip)
python3=$(which python3)
python3_version=$("$python3" --version)
pip3=$(which pip3)

if ! [ -z "$python"]; then
    echo "check python"
    if [ $python_version=="Python 3.6.*" ]; then
        echo "installing required python libraries..."
        $pip install numpy argparse pillow pillow-simd tqdm easydict
    else
        echo "python version is not \"Python 3.6\""
    fi
elif ! [ -z "$python3" ]; then
    echo "check python3"
    if [ $python3_version=="Python 3.6.*" ]; then
        echo "installing required python libraries..."
        $pip3 install numpy argparse pillow pillow-simd tqdm easydict
    else
        echo "python3 version is not \"Python 3.6\""
    fi
fi

echo "Done."
exit 0
