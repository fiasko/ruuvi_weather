# my InfluxDb handler module
from influxdb import InfluxDBClient, exceptions
from datetime import datetime, timedelta
import requests

class InfluxDatabase:
    def __init__(self, ruuvari_setting, data_send_interval = timedelta(seconds=14)):
        self._db_client = InfluxDBClient(host=ruuvari_setting['influx_db_address'],
                                        port=ruuvari_setting['influx_db_port'],
                                        username=ruuvari_setting['influx_db_username'],
                                        password=ruuvari_setting['influx_db_password'],
                                        database=ruuvari_setting['influx_db_database'])
        self._data_send_interval = data_send_interval
        self._last_report_table = dict()

    def add_weather_data(self, tag_name, temp_c, humidity, pressure_hPa, battery_mv):
        current_timestamp = datetime.now()
        display_time = current_timestamp.strftime('%H:%M:%S')

        # find new tags
        if tag_name not in self._last_report_table:
            self._last_report_table[tag_name] = datetime.min

        # Check if it's time to send tag data to server.
        if self._last_report_table[tag_name] <= current_timestamp - self._data_send_interval:
            self._last_report_table[tag_name] = current_timestamp

            try:
                insert_request_json = [
                    {
                        "measurement": 'climate',
                        "tags": {
                            "tag": tag_name
                        },
                        "fields": {
                            "temp": float(temp_c),
                            "pressure": float(pressure_hPa),
                            "humidity": int(humidity),
                            "battery": int(battery_mv)
                        }
                    }
                ]
                self._db_client.write_points(insert_request_json)
            except exceptions.InfluxDBServerError:
                print(f'[{display_time}]  exceptions: InfluxDBServerError!')
            except requests.exceptions.ConnectionError:
                print(f'[{display_time}]  exceptions: InfluxDB connection error!')
            except TypeError as e:
                print(f'[{display_time}]  exceptions: TypeError: {e}')
