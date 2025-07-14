# dryspace-vent

## ESP32 MicroPython project for humidity and odor ventilation control

![dryspace-vent](https://raw.githubusercontent.com/stevendejongnl/dryspace-vent/refs/heads/main/dryspace-vent-logo.png)

## Deploying to your ESP (ESP32/ESP8266)

All commands below are available as Makefile targets. Adjust the `PORT` variable if your ESP is on a different serial port (default: `/dev/ttyUSB0`).

1. **Install MicroPython on your ESP:**
   - Download the latest MicroPython firmware for your board from https://micropython.org/download/ and save as `firmware.bin` in this directory.
   - Run:
     ```sh
     make flash
     ```

2. **Install mpremote:**
   - Run:
     ```sh
     make mpremote-install
     ```

3. **Upload project files:**
   - Run:
     ```sh
     make upload
     ```

4. **Reset your ESP:**
   - Run:
     ```sh
     make reset
     ```

Your ESP should now run the code automatically on boot.
