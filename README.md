https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe # to install python

python -m venv venv # to create a virtual environment

venv\Scripts\activate # to activate the virtual environment before all manipulations

pip install -r requirements.txt # to install the dependencies

pip list # to verified the list of installed dependencies
normal output:
Package            Version
------------------ ---------
alembic            1.18.4
annotated-types    0.7.0
anyio              4.13.0
bcrypt             5.0.0
blinker            1.9.0
certifi            2026.2.25
cffi               2.0.0
charset-normalizer 3.4.7
click              8.3.2
colorama           0.4.6
cryptography       46.0.6
distro             1.9.0
docopt             0.6.2
Flask              3.1.3
Flask-Bcrypt       1.0.1
Flask-Migrate      4.1.0
Flask-SQLAlchemy   3.1.1
greenlet           3.3.2
h11                0.16.0
httpcore           1.0.9
httpx              0.28.1
idna               3.11
itsdangerous       2.2.0
Jinja2             3.1.6
jiter              0.13.0
Mako               1.3.10
MarkupSafe         3.0.3
openai             2.30.0
pip                25.3
pipreqs            0.4.13
pycparser          3.0
pydantic           2.12.5
pydantic_core      2.41.5
PyJWT              2.12.1
PyMySQL            1.1.2
python-dotenv      1.2.2
requests           2.33.1
sniffio            1.3.1
SQLAlchemy         2.0.49
tqdm               4.67.3
typing_extensions  4.15.0
typing-inspection  0.4.2
urllib3            2.6.3
Werkzeug           3.1.8
yarg               0.1.10

python app.py # to run the application