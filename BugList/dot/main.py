import json, os


def write_reporter(graph, bug_id, reporter):
    graph.write(' "{0}" [shape=box style=filled color=".7 .3 1.0"];\n'.format(reporter))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, reporter, 'reporter'))


def write_assigned(graph, bug_id, assigned):
    graph.write(' "{0}" [shape=box style=filled color=".7 .3 1.0"];\n'.format(assigned))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, assigned, 'assigned'))


def write_duplicate(graph, bug_id, duplicate):
    graph.write(' bug_{0} [shape=circle];\n'.format(duplicate))
    graph.write(' bug_{0} -> bug_{1} [label="{2}"];\n'.format(bug_id, duplicate, 'duplicate'))


def write_dependson(graph, bug_id, depend):
    graph.write(' bug_{0} [shape=circle];\n'.format(depend))
    graph.write(' bug_{0} -> bug_{1} [label="{2}"];\n'.format(bug_id, depend, 'dependson'))


def write_blocked(graph, bug_id, block):
    graph.write(' bug_{0} [shape=circle];\n'.format(block))
    graph.write(' bug_{0} -> bug_{1} [label="{2}"];\n'.format(block, bug_id, 'dependson'))


def write_bug(graph, bug_id):
    graph.write(' bug_{0} [shape=circle];\n'.format(bug_id))


def main():
    _set = {}
    with open('items.json', 'r') as data:
        for line in data:
            _json = json.loads(line, encoding='utf-8')
            _set[_json['id']] = {
                'duplicates': _json['duplicates'],
                'dependson': _json['dependson'],
                'flag': False,
                'reporter': _json['reporter'],
                'assigned': _json['assigned'],
                'blocked': _json['blocked']

            }
    index = 0
    for key, val in _set.items():
        e = [key]
        r = set()
        with open('./graph/graph_'+str(index), 'w+', encoding='utf-8') as graph:
            graph.write('digraph G {\n')
            flag = False
            while len(e):
                _index = e.pop()
                if _index in _set.keys():
                    write_bug(graph, _index)
                    write_reporter(graph, _index, _set[_index]['reporter'])
                    write_assigned(graph, _index, _set[_index]['assigned'])
                    r.add(_index)
                    if not _set[_index]['flag']:
                        _duplicates = _set[_index]['duplicates']
                        _dependson = _set[_index]['dependson']
                        _blocked = _set[_index]['blocked']
                        e.extend(_duplicates)
                        e.extend(_dependson)
                        e.extend(_blocked)
                        _set[_index]['flag'] = True
                        for _duplicate in _duplicates:
                            write_duplicate(graph, _index, _duplicate)
                            if _duplicate in _set.keys():
                                write_reporter(graph, _duplicate, _set[_duplicate]['reporter'])
                                write_assigned(graph, _duplicate, _set[_duplicate]['assigned'])
                            flag = True
                        for _depend in _dependson:
                            write_dependson(graph, _index, _depend)
                            if _depend in _set.keys():
                                write_reporter(graph, _depend, _set[_depend]['reporter'])
                                write_assigned(graph, _depend, _set[_depend]['assigned'])
                            flag = True
                        for _block in _blocked:
                            write_blocked(graph, _index, _block)
                            if _block in _set.keys():
                                write_reporter(graph, _block, _set[_block]['reporter'])
                                write_assigned(graph, _block, _set[_block]['assigned'])
                            flag = True
                else:
                    r.add(_index)
            graph.write('}\n')
            graph.flush()
            if not flag:
                graph.close()
                os.remove('./graph/graph_'+str(index))
            else:
                graph.seek(0)
                tmp = graph.readlines()
                addr_to = list(set(tmp))
                addr_to.sort(key=tmp.index)
                graph.seek(0)
                graph.truncate()
                graph.writelines(addr_to)
        index += 1
        for bug in r:
            print(bug, end=',')
        print()


if __name__ == '__main__':
    main()




