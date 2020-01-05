DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PYQT_DEPLOY_BIN=venv/bin

cd "$( dirname "$DIR")" || exit

$PYQT_DEPLOY_BIN/pyqtdeploy-build pyqt-boatswain-linux.pdy
cd build-linux-64 || exit
../sysroot-linux-64/host/bin/qmake
make

cd ..

rm -rf release/linux
mkdir -p release/linux/boatswain
mv build-linux-64/Boatswain release/linux/boatswain/
cp resources/* release/linux/boatswain/

cd release/linux || exit

fpm -s dir -n boatswain -t deb \
          --description "Boatswain is a cross-platform application to manage your docker containers. " \
          boatswain=/usr/local boatswain/boatswain.desktop=/usr/share/applications/
fpm -s dir -n boatswain -t rpm \
          --description "Boatswain is a cross-platform application to manage your docker containers. " \
          boatswain=/usr/local boatswain/boatswain.desktop=/usr/share/applications/

cd ../..