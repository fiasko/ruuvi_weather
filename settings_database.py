import json
import os
import uuid
import socket

default_settings_template = {
        'system_guid':'',
        'system_name': '',

        'master_server_address': '',
        'master_server_port': 0,

        'influx_db_address': '',
        'influx_db_port': 8086,
        'influx_db_username': '',
        'influx_db_password': '',
        'influx_db_database': '',
    }

# public functions
def initialize_settings(settings_database_path):
    if os.path.exists(settings_database_path):
        with open(settings_database_path) as file:
            settings = _verify_and_complete_settings(json.load(file))
        _save_settings_database(settings, settings_database_path)
        return settings
    else:
        directory_name = os.path.dirname(settings_database_path)
        if not os.path.exists(directory_name):
            os.makedirs(directory_name)
        default_settings = create_default_setting()
        _save_settings_database(default_settings, settings_database_path)
        return default_settings

def create_default_setting():
    global default_settings_template
    return _verify_and_set_guid(default_settings_template)

# private functions
def _save_settings_database(settings, path):
    with open(path, 'w') as file:
            json.dump(settings, file, indent=4)

def _verify_and_set_guid(settings):
    if not 'system_guid' in settings or not settings['system_guid']:
        settings['system_guid'] = str(uuid.uuid4())
    if not 'system_name' in settings or not settings['system_name']:
        settings['system_name'] = socket.gethostname()
    return settings

def _verify_and_complete_settings(settings):
    global default_settings_template
    for k, v in default_settings_template.items():
        if not k in settings or not settings[k]:
            settings[k] = default_settings_template[k]
    return default_settings_template | _verify_and_set_guid(settings)

if __name__ == '__main__':
    settings = initialize_settings('cache/settings.json')
    print(settings)
    print(f"System name: {settings['system_name']}")
    print(f"System GUID: {settings['system_guid']}")
