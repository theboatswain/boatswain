DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PYQT_DEPLOY_BIN=venv/bin

cd "$( dirname "$DIR")" || exit

$PYQT_DEPLOY_BIN/pyqtdeploy-build pyqt-boatswain-linux.pdy
cd build-linux-64 || exit
../sysroot-linux-64/host/bin/qmake
make

cd ..

rm -rf release/linux/unix
mkdir -p release/linux/unix
mv build-linux-64/Boatswain release/linux/unix/
cp resources/* release/linux/unix/

cd release/linux || exit

fpm -s dir -t deb unix=/usr/local/boatswain /usr/local/boatswain/boatswain.desktop=/usr/share/applications/
fpm -s dir -t rpm unix=/usr/local/boatswain /usr/local/boatswain/boatswain.desktop=/usr/share/applications/

cd ../..