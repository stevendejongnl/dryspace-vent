.PHONY: venv-create venv-activate install add test flash mpremote-install upload reset

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

upload:
	mpremote connect $(PORT) fs cp main.py :main.py
	mpremote connect $(PORT) fs cp controller.py :controller.py
	mpremote connect $(PORT) fs cp driver.py :driver.py

reset:
	mpremote connect $(PORT) reset
