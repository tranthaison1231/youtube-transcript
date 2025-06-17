.PHONY: dev install

dev:
	python3 -m api.index

install:
	pip install -r requirements.txt
