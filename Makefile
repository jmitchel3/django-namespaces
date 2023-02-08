pip-compile:
	/usr/local/bin/python3.7 requirements/compile.py

venv-pip-install:
	venv/bin/python -m pip install -r requirements/py311-django41.txt

install_django_namespaces:
	venv/bin/python -m pip uninstall django-namespaces -y
	venv/bin/python -m pip install -e . --upgrade --no-cache-dir


check:
	venv/bin/python setup.py sdist bdist_wheel
	venv/bin/twine check dist/*

push:
	venv/bin/python setup.py sdist bdist_wheel
	venv/bin/twine upload dist/*