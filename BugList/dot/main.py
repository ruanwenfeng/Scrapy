import json
_set = {}
with open('items.json', 'r') as data:
    for line in data:
        _json = json.loads(line)
        _set[_json['id']] = {
            'duplicates': _json['duplicates'],
            'dependson': _json['dependson'],
            'flag': False
        }
for key, val in _set.items():
    e = [key]
    r = set()
    while len(e):
        _index = e.pop()

        if _index in _set.keys():
            if not _set[_index]['flag']:
                _duplicates = _set[_index]['duplicates']
                _dependson = _set[_index]['dependson']
                e.extend(_duplicates)
                e.extend(_dependson)
                _set[_index]['flag'] = True
                r.add(_index)
        else:
            r.add(_index)
    for bug in r:
        print(bug, end=',')
    print()

