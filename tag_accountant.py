from datetime import datetime, timedelta

class TagAccountant:
    def __init__(self, tag_detection_timeout = timedelta(seconds=60)):
        self._tag_detection_timeout = tag_detection_timeout
        self._new_tag_list = dict()

    def update(self, tag_name):
        current_timestamp = datetime.now()
        display_time = current_timestamp.strftime("%H:%M:%S")

        # find new tags
        if tag_name not in self._new_tag_list.keys():
            print(f'[{display_time}] New tag detected: {tag_name}')
        
        self._new_tag_list[tag_name] = current_timestamp
        
        # remove dead tags
        removable_tags = []
        for name, time in self._new_tag_list.items():
            if time < current_timestamp - self._tag_detection_timeout:
                print(f'[{display_time}] Lost tag detected: {name}' )
                removable_tags.append(name)
        
        for tag in removable_tags:
            del self._new_tag_list[tag]
            