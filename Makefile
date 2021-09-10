install:
	poetry install
zonehelper:
	poetry run zonehelper
package-install:
	python3 -m pip install --user dist/*.whl
lint:
	poetry run flake8 zonehelper
build:
	make build
.PHONY: install zonehelper lint build package-install
