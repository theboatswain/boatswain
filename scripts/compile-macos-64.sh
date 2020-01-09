DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

PYQT_DEPLOY_BIN=venv/bin

cd "$( dirname "$DIR")" || exit

echo "Enter the release version: "
read -r VERSION

cp boatswain/main.py boatswain/main.py.bak

python scripts/update_version.py boatswain/main.py "${VERSION}"

$PYQT_DEPLOY_BIN/pyqtdeploy-build pyqt-boatswain.pdy
cd build-macos-64 || exit
../sysroot-macos-64/host/bin/qmake
make

cd ..

rm -rf release/macos
mkdir -p release/macos/"${VERSION}"
mv build-macos-64/Boatswain.app release/macos/"${VERSION}"
cp resources/* release/macos/"${VERSION}"/Boatswain.app/Contents/Resources/

rm -rf release/macos/"${VERSION}"/Boatswain.app/Contents/Resources/*.desktop

python scripts/zipping.py release/macos/"${VERSION}"/Boatswain.app x64 "${VERSION}"

mv boatswain/main.py.bak boatswain/main.py