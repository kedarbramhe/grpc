import json
import keyval_pb2

FILENAME = "keyval.json"

def read_keyval_database():
    """Reads the key val database.
  """
    feature_list = {}
    try:
        with open(FILENAME) as handle:
            for item in json.load(handle):
                feature = keyval_pb2.Entry(key= item['key'],value= item['value'],current_version=item['version'])
                feature_list[item['key']] = feature
    except:
        with open(FILENAME, 'wb') as handle:
            json.dump(feature_list, handle)

    return feature_list



