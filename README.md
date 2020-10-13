# Connect-Shelly-to-Wifi

## Problem

* Out of the Box Shelly devices are in AP mode and not connected to the home wifi - they create their own wifi network.
* You need to connect each Shelly device manually one-by-one using the Shelly app to your home wifi.
* After converting the Shelly OS to new direct HomeKit firmware the Shelly app no longer necessary - [link](https://github.com/mongoose-os-apps/shelly-homekit)

## Purpose of this

  * Connect all shelly devices to your home wifi network at once without having to download the Shelly app.
  * you can use @andyblac Tool in mongoose-os-apps/shelly-homekit/tools to convert all shelly devices to new firmware at once.

## What will happen

Running this python file will search for all nearby shelly device(s) that are in AP mode (you should be in close range to the shelly device(s), and connect each of them to your home wifi - your wifi password will be required.

## When you run the script make sure:
* wifi is on
* you are connected to your home wifi
* you are in wifi range to all shelly devices

## Supported OS:
* macOS
