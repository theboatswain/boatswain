DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PYQT_DEPLOY_BIN=venv/bin

cd "$( dirname "$DIR")" || exit

VERSION="$(python scripts/get_version.py boatswain/main.py)"

$PYQT_DEPLOY_BIN/pyqtdeploy-build pyqt-boatswain.pdy
cd build-macos-64 || exit
../sysroot-macos-64/host/bin/qmake
make

cd ..

rm -rf release/macos
mkdir -p release/macos/"${VERSION}"
mv build-macos-64/Boatswain.app release/macos/"${VERSION}"
cp -R resources/* release/macos/"${VERSION}"/Boatswain.app/Contents/Resources/

rm -rf release/macos/"${VERSION}"/Boatswain.app/Contents/Resources/*.desktop

python scripts/zipping.py release/macos/"${VERSION}"/Boatswain.app x64 "${VERSION}"
