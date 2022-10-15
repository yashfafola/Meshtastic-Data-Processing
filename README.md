## meshtastc_tester
* This program is created for automatic testing the LoRa devices equipped with meshtastic firmware.
* This program runs on top of meshtastic-python (CLI) library.
* The purpose of this app is to do flexible and automatic tests in different scenarios to analyse LoRa mesh network.
* Credit for firmware goes to respective developers and contributors.
* Tx data can be saved by `Export CSV` button, Rx data would be available on the other LoRa device which can be accessed via webapp.
* A LoRa device should be connected serially to a computer running this app.

![meshtastic_tester GUI](/image/meshtastic_tester_GUI.png) 

## mehstasticdataprocessing
* This program is created to convert the recorded serial logs of a LoRa device running meshtastic firmware into pretty excel format, extracting usefull data.
* Select log file by clicking `Serial Logs` button.
* Get csv output by clicking `Process Serial Logs`

![meshtasticdataprocessing GUI](/image/meshtasticdataprocessing_GUI.png) 