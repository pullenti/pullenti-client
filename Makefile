
IMAGE = pullenti/pullenti-server

deamon:
	docker run -d -p 8080:8080 $(IMAGE)

run:
	docker run -it --rm -p 8080:8080 $(IMAGE)

clean:
	find pullenti_client -name '*.pyc' -not -path '*/__pycache__/*' -o -name '.DS_Store*' | xargs rm
	rm -rf dist build *.egg-info
