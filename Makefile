VENV_PATH := /home/vagrant/venv/bin

runserver:
	$(VENV_PATH)/python manage.py runserver 0.0.0.0:8000

start:
	$(VENV_PATH)/gunicorn --preload -D -b 127.0.0.1:8000 starreditemsbot.wsgi:application

pep8:
	$(VENV_PATH)/pep8 --exclude=*migrations*,*settings_local.py* --max-line-length=119 --show-source  starreditemsbot/

pyflakes:
	$(VENV_PATH)/pylama --skip=*migrations* -l pyflakes starreditemsbot/

lint:
	make pep8
	make pyflakes

test:
	$(VENV_PATH)/python manage.py test -v 2 --noinput

ci_test:
	make test
	make lint

wheel_install:
	$(VENV_PATH)/pip install --no-index -f wheels/ -r requirements.txt

