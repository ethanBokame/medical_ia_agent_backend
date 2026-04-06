https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe # to install python

python -m venv venv # to create a virtual environment

venv\Scripts\activate # to activate the virtual environment before all manipulations

pip install -r requirements.txt # to install the dependencies

pip list # to verified the list of installed dependencies
normal output:
Package            Version
------------------ ---------
blinker            1.9.0
certifi            2026.2.25
charset-normalizer 3.4.7
click              8.3.2
colorama           0.4.6
Flask              3.1.3
idna               3.11
itsdangerous       2.2.0
Jinja2             3.1.6
MarkupSafe         3.0.3
pip                25.3
requests           2.33.1
urllib3            2.6.3
Werkzeug           3.1.8

flask run # to run the application