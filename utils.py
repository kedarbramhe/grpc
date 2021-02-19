import json
import keyval_pb2

FILENAME = "keyval.json"

def read_keyval_database(filename = FILENAME):
    """Reads the key val database.
  """
    feature_list = {}
    try:
        with open(filename) as handle:
            for item in json.load(handle):
                feature = keyval_pb2.Entry(key= item['key'],value= item['value'],current_version=item['current_version'])
                feature_list[item['key']] = feature
    except:
        with open(filename, 'w') as handle:
            json.dump([], handle)

    return feature_list


def save_keyval_database(db, filename = FILENAME):
    final = []
    for key, val_obj in db.items():
        item = {"key": key, "value":val_obj.value, "current_version":val_obj.current_version}
        final.append(item)
    print('writing to json file: {}'.format(final))
    with open(filename, 'w') as handle:
            json.dump(final, handle)
