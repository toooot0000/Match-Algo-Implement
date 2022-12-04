PY_VERSION=$(python3 -V)
PY_VERSION=${PY_VERSION##'Python '}
echo "Current python version: $PY_VERSION"
PY_MAJOR=${PY_VERSION%%\.*}
PY_VERSION=${PY_VERSION#*\.}
PY_MINOR=${PY_VERSION%%\.*}
PY_PATCH=${PY_VERSION#*\.}

if (($PY_MAJOR <= 3)) && !(($PY_MAJOR == 3 && $PY_MINOR > 9)) && !(($PY_MAJOR == 3 && $PY_MINOR == 9 && $PY_PATCH >=1))
then
    echo "!!!WARNING: Python version is lower than 3.9.1. Can't guarantee that the script can work!!!"
    echo "Please update your python! Or use a vitual environment!"
fi

pip3 install -r requirements.txt
python3 efficient.py input.txt output.txt