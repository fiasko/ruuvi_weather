# Ruuvi Weather Station
Ruuvi tag weather data receiver. Receives the data transmitted by Ruuvi tags and forwards the weather data to Influx DB (remote or local). Project target environment is Raspberry PI, but should work in most Linux environments where ruuvitag-sensor python module works.

# Dependencies
- Python 3
- bluez-hcidump (ruuvitag-sensor dependency)
- ruuvitag-sensor python module
- influxdb python module
- bleak python module

  
