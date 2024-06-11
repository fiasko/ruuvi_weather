import json
import os

def read_tag_info_database(database_file):
    if os.path.exists(database_file):
        with open(database_file) as f:
            tag_database = json.load(f)

        if 'tag_info' in tag_database:
            return tag_database['tag_info']
    return dict()

if __name__ == '__main__':
    tag_info_database_file = 'cache/tags_info.json'
    tag_database = read_tag_info_database(tag_info_database_file)
    if tag_database is None:
        print(f'Database "{tag_info_database_file}" read failed!')
    else:
        print('Database content')
        print(tag_database)
