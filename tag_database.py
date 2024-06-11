import json
import os
from datetime import datetime, timedelta

# clean tags older than threshold days from the database
dead_tag_threshold_days = 7
tag_date_format = '%Y-%m-%d'

class TagDatabase:
    def __init__(self, file_path, list_name):
        self._file_path = file_path
        self._last_file_modified_timestamp = None
        self._list_name = list_name
        self._data = {}
        self.reload_database()
    
    def reload_database(self):
        if os.path.exists(self._file_path):
            file_mod_time = os.path.getmtime(self._file_path)
            if file_mod_time != self._last_file_modified_timestamp:
                self._last_file_modified_timestamp = file_mod_time
                try:
                    with open(self._file_path, 'r') as file:
                        self._data = json.load(file)
                    print(f"Database reloaded from {self._file_path}.")
                except json.decoder.JSONDecodeError:
                    print(f"Database reload error. Creating new.")
                    self._data = {self._list_name: []}
            else:
                print(f"Database reloaded skipped. Database not modified.")
        else:
            self._data = {self._list_name: []}
            print(f"No existing database found. Created a new empty database.")

    def is_tag_in_database(self, tag_id, tag_key=None):
        if tag_key:
            return any(tag[tag_key] == tag_id for tag in self._data[self._list_name])
        else:
            return tag_id in self._data.get(self._list_name, [])

    def update_tag_info(self, tag_id, tag_key, update_date=False):
        global tag_date_format
        current_date = datetime.now().strftime(tag_date_format)
        if not self.is_tag_in_database(tag_id, tag_key):
            self._data[self._list_name].append({tag_key:tag_id, "last_seen":current_date})
            self._save_database()
            print(f"Tag '{tag_id}' added to the database.")
        elif update_date:
            for tag in self._data[self._list_name]:
                if tag[tag_key] == tag_id:
                    if tag["last_seen"] != current_date:
                        tag["last_seen"] = current_date
                        self._save_database()
                        print(f"Tag '{tag_id}' 'last_seen' info updated in the database")
        else:
            print(f"Tag '{tag_id}' info not updated in the database.")
    
    def _remove_old_tags(self):
        global dead_tag_threshold_days
        global tag_date_format
        threshold_date = datetime.now() - timedelta(days=dead_tag_threshold_days)
        
        new_tag_list = []
        list_modified = False
        for tag in self._data[self._list_name]:
            last_seen_date = datetime.strptime(tag['last_seen'], tag_date_format)
            if last_seen_date >= threshold_date:
                new_tag_list.append(tag)
                list_modified = True
        if list_modified:
            self._data[self._list_name] = new_tag_list
            self._save_database()

    def _save_database(self):
        with open(self._file_path, 'w') as file:
            json.dump(self._data, file, indent=4)
        print(f"Database saved to {self._file_path}.")
        self._last_file_modified_timestamp = os.path.getmtime(self._file_path)


# Example usage
if __name__ == '__main__':
    test_tag_list = [
        'CC:20:DE:12:34:56',
        'C8:3C:63:12:34:56',
        'D5:17:35:12:34:56',
        # 'FC:34:B1:12:34:56',
        # 'CD:07:4E:12:34:56',
        # 'DC:89:51:12:34:56',
        # 'F7:9C:73:12:34:56',
        'CB:D0:F6:12:34:56',
        'E1:A0:2D:12:34:56',
    ]

    db = TagDatabase('cache/tags_known.json', 'tag_list')
    db.reload_database()

    for t in test_tag_list:
        #print(db.is_tag_in_database(t, 'mac'))
        db.update_tag_info(t, 'mac', update_date=True)
