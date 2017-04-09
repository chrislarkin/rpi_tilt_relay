# Tilt Hydrometer data relay

The [Tilt](https://tilthydrometer.com) is a wireless hydrometer that supports the logging of temperature and gravity data to the cloud via Google Sheets. This repo extends the cloud logging capabilities present in the official Android/iOS apps to the Pi (or any computer with the requisite hardware/software). It borrows from sibowler's [brewpi-brewometer](https://github.com/sibowler/brewpi-brewometer), which is a fantastic repo for anyone interested in using the Tilt as a [brewpi](https://github.com/BrewPi/) sensor.

### Setup

 * Make sure you have the necessary libraries:
 
   `sudo apt-get install bluez python-bluez python-scipy python-numpy`

   
 * Enable python to query bluetooth without being root:
 
   `sudo setcap cap_net_raw+eip $(eval readlink -f \`which python\`)`
 
 
 * Clone this repo
 
 
 * Update the global variables in [relay.py](https://github.com/chrislarkin/rpi_tilt_relay/blob/master/relay.py) to include the address to your Google Sheet, the color of the Tilt you wish to track, and an optional logfile location


 * (Optionally) Enable [calibration](https://github.com/sibowler/brewpi-brewometer/blob/master/README.md#calibration) in the [config](https://github.com/chrislarkin/rpi_tilt_relay/blob/master/config) folder


 * Run (or set as a `cron`):

   `python relay.py` 