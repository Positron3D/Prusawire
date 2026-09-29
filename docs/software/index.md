---
layout: default
title: Software Overview
has_children: true
nav_order: 7
---

# Software Overview

## Klipper Configuration Files

The most up–to–date Klipper configuration files for setting up or updating the Prusawire are in our [config repository](https://github.com/Positron3D/prusawire-klipper-config).

## Upgrading the Einsy Rambo to Klipper - Read this

Installing Klipper on the Einsy Rambo board is possible, with extra steps. Follow the guide [published by the awesome folks at MyRigs3D](https://myrigs3d.com/blogs/infos/revive-your-prusa-mk3s-with-klipper-1-5-flash-bootloader)! We recommend Method 2.

**Note:** Some users have reported problems using `avrdude` with the latest Raspberry Pi OS version (bookworm). If you experience error messages from avrdude complaining about gpio ports being busy, please try using the bullseye version of Raspberry Pi OS instead, available as "Raspberry Pi OS (Legacy)" in Raspberry Pi Imager.

If the legacy OS method above doesn't work - please see the Troubleshooting section at the bottom of this doc for detailed instructions on a workaround. 

## Resources
- [Voron Software Installation Guide](https://docs.vorondesign.com/build/software/) for some good resources on Mainsail (Klipper on Raspberry Pi) and Control Board firmware.
- [Raspberry Pi OS based \| MainsailOS](https://docs-os.mainsail.xyz/getting-started/raspberry-pi-os-based)
- [Welcome to Mainsail \| Mainsail](https://docs.mainsail.xyz/)
- [GitHub - bigtreetech/BIGTREETECH-SKR-mini-E3](https://github.com/bigtreetech/BIGTREETECH-SKR-mini-E3)
- [BIGTREETECH-SKR-mini-E3/firmware/V3.0/Klipper at master · bigtreetech/BIGTREETECH-SKR-mini-E3 · GitHub](https://github.com/bigtreetech/BIGTREETECH-SKR-mini-E3/tree/master/firmware/V3.0/Klipper)

## Configuration
Start with the [Positron3D Prusawire Configuration](https://github.com/Positron3D/prusawire-klipper-config) settings and profiles.

More detail general instructions are found at [Software Configuration \| Voron Documentation](https://docs.vorondesign.com/build/software/configuration.html).

### Sensorless Homing
If you are running the Einsy board, congrats, you are now done.

For the BTT SKR Mini E3, some further tuning likely needs to happen. Refer to [this guide](https://gist.github.com/clee/9108f7717defce8b1222698f816def0a#finding-the-right-stallguard-threshold) by clee on setting the correct stallguard threshold.
### Input Shaper
Some defaults have been provided, but they are no doubt unsuitable for your exact machine. We recommend installing [ShakeTune](https://github.com/Frix-x/klippain-shaketune) for measuring resonances, and reading the [Klipper guide](https://www.klipper3d.org/Measuring_Resonances.html#max-smoothing) on understanding which value to choose.

**Y Axis Input Shaping**: This requires an external accelerometer (eg LDO Input Shaper) to be mounted to your heated bed.

# Troubleshooting
## Einsy Klipper - AVRDude GPIO Busy
The following workaround has been verified on both a Rapberry Pi 3 Model B and a Raspberry Pi 4. It is an extension of the Method 2 by [MyRigs3D](https://myrigs3d.com/blogs/infos/revive-your-prusa-mk3s-with-klipper-1-5-flash-bootloader) with the latest version of `avrdude`.

Pre-Requisites: 
- Pi OS: Latest or MainsailOS
- `avrdude.conf` is not modified
- GPIO pins are connected as described in Method 2

Steps:
1. SSH into your pi and install libgpiod-dev: via `sudo apt-get install -y libgpiod-dev`
2. Install the latest version of avrdude from github and build it on your machine (don't worry if you have the prev avrdude version still installed)
```
sudo apt-get install build-essential git cmake flex bison pkg-config libelf-dev libusb-dev libhidapi-dev libftdi1-dev libreadline-dev libserialport-dev

git clone https://github.com/avrdudes/avrdude.git
cd avrdude
./build.sh

cmake -D CMAKE_BUILD_TYPE=RelWithDebInfo -D HAVE_LINUXGPIO=1 -D HAVE_LINUXSPI=1 -B build_linux

# install linuxgpio if it's missing
sudo apt-get install linuxgpio

cmake --build build_linux

sudo cmake --build build_linux --target install
```
3. Reboot your pi `sudo reboot`
4. Do not edit the avrdude conf file directly, instead create a config file `nano ~/pi_1.conf`
5. Paste this into the config file - Note the mappings are now different (mosi -> sdo,  miso -> sdi)
```
programmer
    id = "pi_1";
    desc = "Raspberry Pi GPIO ISP programmer";
    type = "linuxgpio";
    connection_type = linuxgpio;
    prog_modes = PM_ISP;
    reset = 12;
    sck = 24;
    sdo = 23;
    sdi = 18;
;
```
**Important** - Because you've added this custom config file, the next commands must include both references to both.

**Important** - The following commands include a tag called `<hostname>`. You **should not directly copy paste this value**. This is a placeholder for **your** pi's hostname that you configured when you flashed the OS.

7. Run the updated firmware backup command with your hostname
```
sudo avrdude \
-C /usr/local/etc/avrdude.conf \
-C +/home/<hostname>/pi_1.conf \
-p m32u2 \
-F \
-c pi_1 \
-U flash:r:firmware_backup.hex:i \
-U eeprom:r:eeprom.hex:i \
-U lfuse:r:lowfuse:h \
-U hfuse:r:highfuse:h \
-U efuse:r:exfuse:h \
-U lock:r:lockfuse:h
```

8. Run the updated fuse command with your hostname
```
sudo avrdude -C /usr/local/etc/avrdude.conf -C +/home/<hostname>/pi_1.conf -p m32u2 -F -c pi_1 -U hfuse:w:0xD1:m
```
9. Download the prusa flashware `wget https://raw.githubusercontent.com/PrusaOwners/mk3-32u2-firmware/master/hex_files/DFU-hoodserial-combined-PrusaMK3-32u2.hex`

10. Run the updated flash firmware command with your hostname
```
sudo avrdude \
  -C /usr/local/etc/avrdude.conf \
  -C +/home/<hostname>/pi_1.conf \
  -p m32u2 \
  -F \
  -c pi_1 \
  -U flash:w:DFU-hoodserial-combined-PrusaMK3-32u2.hex \
  -U lfuse:w:0xFF:m \
  -U hfuse:w:0xD9:m \
  -U efuse:w:0xF4:m
```
11. Shut down the pi `sudo shutdown -r now` and disconnect all GPIO cables. 