run:
	python3 ./pinger.py

setup:
	python3 -m pip install -r requirements.txt

test:
	python3 -m pytest --cov=pinger --cov-report=xml:cov.xml --cov-report=html:htmlcov test_pinger.py
