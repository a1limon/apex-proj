sudo apt-get update
sudo apt install awscli
sudo apt install python3-pip python3-dev
pip3 install --upgrade pip
export PATH="$PATH:/home/ubuntu/.local/bin"
sudo apt-get install python3-venv
python3 -m venv env
source env/bin/activate
# git clone
pip install -r ~/dsc102-bert/requirements.txt
