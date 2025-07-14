# dryspace-vent

## ESP32 MicroPython project for humidity and odor ventilation control

![dryspace-vent](https://raw.githubusercontent.com/stevendejongnl/dryspace-vent/refs/heads/main/dryspace-vent-logo.png)

## Deploying to your ESP (ESP32/ESP8266)

All commands below are available as Makefile targets. Adjust the `PORT` variable if your ESP is on a different serial port (default: `/dev/ttyUSB0`).

1. **Install MicroPython on your ESP:**
   - Download the latest MicroPython firmware for your board from https://micropython.org/download/ and save it as `firmware.bin` in this directory.
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
   - See the section below for uploading master.py and slave.py to the correct ESP board.

4. **Reset your ESP:**
   - Run:
     ```sh
     make reset
     ```

Your ESP should now run the code automatically on boot.

## Using master and slave

This project supports a master-slave setup with two ESP boards:
- The **master** device runs the main controller logic.
- The **slave** device acts as a remote sensor or actuator and communicates with the master.

### Uploading to the correct ESP

1. Connect the ESP you want to use as the master.
2. Upload the master code:
   ```sh
   make upload-master
   ```
3. Connect the ESP you want to use as the slave.
4. Upload the slave code (replace <MASTER_IP> with the actual IP address of your master ESP):
   ```sh
   make upload-slave MASTER_IP=<MASTER_IP>
   ```

Repeat the other steps from the 'Deploying to your ESP' section for both ESPs if needed.
