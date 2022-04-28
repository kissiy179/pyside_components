rmdir /s /q .venv
python3 -m venv .venv
call .venv\scripts\activate.bat
pip install -e .
pip install jupyterlab