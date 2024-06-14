import os
# set environment variable for Ruuvitag sensor
os.environ["RUUVI_BLE_ADAPTER"] = "bleak"

import asyncio
from datetime import datetime, timedelta
from ruuvitag_sensor.ruuvi import RuuviTagSensor
from my_influx_db import InfluxDatabase
from tags_info_database import read_tag_info_database
from tag_database import TagDatabase
from settings_database import initialize_settings
from tag_accountant import TagAccountant

# Global settings
# Information from known tags
weather_station_settings_database_path= 'cache/settings.json'
tags_info_database_path= 'cache/tags_info.json'
tags_detected_database_path = "cache/tags_detected.json"
tags_foreign_database_path = "cache/tags_foreign.json"

## Load current tag info
app_settings = initialize_settings(weather_station_settings_database_path)
tag_info_database = read_tag_info_database(tags_info_database_path)
detected_tags_database = TagDatabase(tags_detected_database_path, "tag_list")
foreign_tags_database = TagDatabase(tags_foreign_database_path, "tag_list")

influxdb = None
if 'influx_db_address' in app_settings and app_settings['influx_db_address'] and 'influx_db_port' in app_settings and app_settings['influx_db_port'] != 0:
    print("Influx DB configured")
    influxdb = InfluxDatabase(ruuvari_setting=app_settings)
else:
    print("Influx DB not configured!")

print(f"Starting weather station: {app_settings['system_name']}")

# Runtime list detected tags
tag_accountant = TagAccountant(tag_detection_timeout=timedelta(seconds=60))
current_date_prev = ""

async def main():
    global tag_info_database
    global detected_tags_database
    global foreign_tags_database
    global current_date_prev
    global influxdb

    async for found_data in RuuviTagSensor.get_data_async():
        current_date = datetime.now().strftime("%a %d.%m.%Y")
        if current_date_prev != current_date:
            print(f"[{current_date}]")
            current_date_prev = current_date

        detected_tags_database.update_tag_info(found_data[0], tag_key='mac', update_date=True, tag_rssi=found_data[1]['rssi'])

        if foreign_tags_database.is_tag_in_database(found_data[0]):
            print(f'Foreign tag detected: {found_data[0]}')
            return
        else:
            tag_info = next((tag for tag in tag_info_database if tag["mac"] == found_data[0]), None)
            if tag_info:
                if tag_info['ingore']:
                    print (f'Tag name: { tag_info["name"] } (ignored)')
                    return
                else:
                    tag_accountant.update(tag_info['name'])
            else:
                print(f'Unkown tag found! ignoring results: {found_data[0]}')
                return

        # Data for Influxdb module
        if influxdb:
            influxdb.add_weather_data(tag_info['name'], found_data[1]['temperature'], found_data[1]['humidity'], found_data[1]['pressure'], found_data[1]['battery'])

# Start monitoring Ruuvi tags
if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
