# Ruuvi Weather Station
Ruuvi tag weather data receiver. Receives the data transmitted by Ruuvi tags and forwards the weather data to Influx DB (remote or local). Project target environment is Raspberry PI, but should work in most Linux environments where ruuvitag-sensor python module works.

# Dependencies
- Python 3
- bluez-hcidump (ruuvitag-sensor dependency)
- [RuuviTag Sensor](https://github.com/ttu/ruuvitag-sensor) python package
- [InfluxDB-Python](https://github.com/influxdata/influxdb-python) python package
- [bleak](https://github.com/hbldh/bleak) python package

  
# Settings
settings.json
- Contains initial settings for the weather station platform
- connection settings to master server and  influxdb server

tags_detected.json
- database for tags detected by the weather stations
- includes dynamic values of tag RSSI

tags_foreign.json
- includes tags tha you don't want to monitor

tags_info.json
- includes info from monitored tags