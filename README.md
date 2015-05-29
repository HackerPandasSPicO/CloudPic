# Cloud-Photos-Organizer

Installation
=======================

1. Install virtualenv:
    `easy_install virtualenv`
2. Create a new environment:
    `virtualenv --python=python3 env`
3. Activate the environment:
    [https://virtualenv.pypa.io/en/latest/userguide.html#activate-script](https://virtualenv.pypa.io/en/latest/userguide.html#activate-script)

    For Windows: `env/bin/actiate.bat` or `python env/bin/activate_this.py`
    For Linux: `source env/bin/activate`
4. Install all required packages:
    `pip install -r requirements.txt`
5. Syncdb:
    `python manage.py syncdb`
6. Run:
    `python manage.py runserver`