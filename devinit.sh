# this script is supposed to be executed as postCreateCommand of the devcontainer
pip3 install -r requirements_dev.txt 
pip3 install -e .
if [ -f setuplinks.sh ]; then
    . ./setuplinks.sh
fi