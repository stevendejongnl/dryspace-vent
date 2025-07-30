.PHONY: venv-create venv-activate install add test flash mpremote-install upload reset black flake8 mypy install-lint

venv-create:
	python -m venv .venv
	.venv/bin/pip install --upgrade pip

venv-activate:
	@echo "To activate the virtual environment, run:"
	@echo "source .venv/bin/activate"

install: venv-create
	.venv/bin/pip install poetry
	.venv/bin/poetry install --no-root

add:
ifndef package
	$(error Please provide a package name: make package-add package=packagename)
endif
	.venv/bin/poetry add $(package)

test:
	.venv/bin/poetry run pytest

# ESP32/ESP8266 settings
PORT ?= /dev/ttyUSB0
FIRMWARE ?= firmware.bin

flash:
	@echo "Flashing MicroPython firmware to $(PORT) using $(FIRMWARE)"
	esptool.py --port $(PORT) erase_flash
	esptool.py --port $(PORT) --baud 460800 write_flash -z 0x1000 $(FIRMWARE)

mpremote-install:
	pip install --user mpremote

upload-master:
	mpremote connect $(PORT) fs cp src/main.py :main.py
	mpremote connect $(PORT) fs cp src/master.py :master.py
	mpremote connect $(PORT) fs cp src/controller.py :controller.py
	mpremote connect $(PORT) fs cp src/driver.py :driver.py
	mpremote connect $(PORT) fs cp src/slave.py :slave.py
	mpremote connect $(PORT) fs cp src/config.py :config.py

upload-slave:
	ifndef MASTER_IP
		$(error Please provide MASTER_IP: make upload-slave MASTER_IP=192.168.1.100)
	endif
	mpremote connect $(PORT) fs cp src/main.py :main.py
	mpremote connect $(PORT) fs cp src/slave.py :slave.py
	mpremote connect $(PORT) fs cp src/controller.py :controller.py
	mpremote connect $(PORT) fs cp src/driver.py :driver.py
	mpremote connect $(PORT) fs cp src/master.py :master.py
	mpremote connect $(PORT) fs cp src/config.py :config.py

log:
	mpremote connect $(PORT) repl

reset:
	mpremote connect $(PORT) reset

black:
	.venv/bin/black .

flake8:
	.venv/bin/flake8 . --exclude=.venv,site-packages --ignore=E501,W503

mypy:
	.venv/bin/mypy src
	.venv/bin/mypy scripts

install-lint:
	.venv/bin/pip install black flake8 mypy

config:
	python3 scripts/config_wizard.py
