VENV_PATH := /home/vagrant/venv/bin

runserver:
	killall -9 python
	$(VENV_PATH)/python tlgrm_runner.py

start:
	( ( nohup $(VENV_PATH)/python tlgrm_runner.py > /dev/null 2> /dev/null 2>&1 ) & )

pep8:
	$(VENV_PATH)/pep8 --exclude=*migrations*,*settings_local.py* --max-line-length=119 --show-source  starreditemsbot/

pyflakes:
	$(VENV_PATH)/pylama --skip=*migrations* -l pyflakes starreditemsbot/

lint:
	make pep8
	make pyflakes

test:
	# pass

ci_test:
	make test
	make lint

wheel_install:
	$(VENV_PATH)/pip install --no-index -f wheels/ -r requirements.txt
