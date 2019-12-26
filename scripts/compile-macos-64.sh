DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PYQT_DEPLOY_BIN=venv/bin

cd "$( dirname "$DIR")" || exit

$PYQT_DEPLOY_BIN/pyqtdeploy-build pyqt-boatswain.pdy
cd build-macos-64 || exit
../sysroot-macos-64/host/bin/qmake
make

cd ..

mkdir -p release/macos
mv build-macos-64/Boatswain.app release/macos/
cp resources/* release/macos/Boatswain.app/Contents/Resources/