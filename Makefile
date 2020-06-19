run:
	python3 ./pinger_runner.py

setup:
	python3 -m pip install -r requirements.txt

test: lint
	python3 -m pytest --cov=pinger --cov-report=xml:cov.xml --cov-report=html:htmlcov tests/test_*.py

build:
	python3 setup.py build

clean:
	python3 setup.py clean
	rm -rf build pinger.egg-info dist htmlcov __pycache__

install: build test lint
	python3 setup.py install

lint:
	flake8 pinger tests
