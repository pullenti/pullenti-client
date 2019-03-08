
IMAGE = pullenti/pullenti-server:3.17

up:
	docker run --name pullenti -d -p 8080:8080 $(IMAGE)

down:
	docker rm -f pullenti

tag:
	git tag `python version.py get setup.py`

version:
	python version.py inc setup.py

wheel:
	python setup.py bdist_wheel --universal

upload:
	twine upload dist/*

test:
	pytest --pep8 --flakes pullenti_client --nbval-lax -v docs.ipynb

clean:
	find pullenti_client -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
