cd install/
tar xvf Python-$VERSION.tgz
cd Python-$VERSION/
./configure --enable-optimizations
sudo make altinstall
export PATH=$PATH:/usr/local/bin
sudo yum install python-virtualenv
virtualenv -p python3.8 .env
source .env/bin/activate
pip install -r requirements.txt
