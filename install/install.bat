:: Initial Install Script for 447-scheduler

:: Install Python WIP
python-3.7.0.exe /quiet InstallAllUsers=1 PrependPath=1 Include_test=0

:: Install Pip
curl https://bootstrap.pypa.io/get-pip.py > get-pip.py
python get-pip.py

:: Install Flask Dependencies
pip install flask
pip install flask-restful
pip install flask-cors

:: Install OR-Tools
python -m pip install --user ortools

