import json


class JsonObject:

    def __init__(self, json_data):
        self.json_data = json_data

    def find_json_key(self, key):

        results = []
        in_json = json.dumps(self.json_data)

        def iterate_json(a_dict):
            try:
                results.append(a_dict[key])
            except KeyError:
                pass
            return a_dict

        json.loads(in_json, object_hook=iterate_json)
        return results[0]
