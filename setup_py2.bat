rmdir /s /q .venv
python2 -m pip install virtualenv
python2 -m virtualenv .venv
call .venv\scripts\activate.bat
pip install -e .