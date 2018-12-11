
IMAGE = pullenti/pullenti-server

deamon-server:
	docker run -d -p 8080:8080 $(IMAGE)

server:
	docker run -it --rm -p 8080:8080 $(IMAGE)

test:
	pytest --pep8 --flakes pullenti_client --nbval-lax -v docs.ipynb

clean:
	find pullenti_client -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
