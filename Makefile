
IMAGE = pullenti/pullenti-server:3.19

up:
	docker run --name pullenti -d -p 8080:8080 $(IMAGE)

down:
	docker rm -f pullenti

version:
	bumpversion minor

wheel:
	python setup.py bdist_wheel

upload:
	twine upload dist/*

test:
	pytest --pep8 --flakes pullenti_client --nbval-lax --current-env -v docs.ipynb

clean:
	find pullenti_client -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
