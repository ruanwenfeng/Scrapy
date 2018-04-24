import json, os


def write_reporter(graph, bug_id, reporter):
    graph.write(' "{0}" [shape=box style=filled color=".7 .3 1.0"];\n'.format(reporter))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, reporter, 'reporter'))


def write_assigned(graph, bug_id, assigned):
    graph.write(' "{0}" [shape=box style=filled color=".7 .3 1.0"];\n'.format(assigned))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, assigned, 'assigned'))


def write_cc(graph, bug_id, cc):
    graph.write(' "{0}" [style=filled color=".3 .7 1.0"];\n'.format(cc))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, cc, 'cc'))


def write_platform(graph, bug_id, platform):
    graph.write(' "{0}" [style=filled color=".3 .3 1.0"];\n'.format(platform))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, platform, 'platform'))


def write_sys(graph, bug_id, sys):
    graph.write(' "{0}" [style=filled color=".3 1.0 0.3"];\n'.format(sys))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, sys, 'sys'))


def write_creation_ts(graph, bug_id, creation_ts):
    graph.write(' "{0}" [style=filled color=".3 1.0 0.7"];\n'.format(creation_ts))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, creation_ts, 'creation_ts'))


def write_modified(graph, bug_id, modified):
    graph.write(' "{0}" [style=filled color=".3 0.5 2"];\n'.format(modified))
    graph.write(' bug_{0} -> "{1}" [label="{2}"];\n'.format(bug_id, modified, 'modified'))


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


def write_attr(graph, bug_id, bug_data):
    write_reporter(graph, bug_id, bug_data['reporter'])
    write_assigned(graph, bug_id, bug_data['assigned'])
    write_cc(graph, bug_id, bug_data['cc'])
    write_platform(graph, bug_id, bug_data['platform'])
    write_sys(graph, bug_id, bug_data['sys'])
    write_creation_ts(graph, bug_id, bug_data['creation_ts'])
    write_modified(graph, bug_id, bug_data['modified'])


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
                'cc': _json['cc'],
                'platform': _json['platform'],
                'sys': _json['sys'],
                'creation_ts': _json['creation_ts'],
                'modified': _json['modified'],
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
                    # write_reporter(graph, _index, _set[_index]['reporter'])
                    # write_assigned(graph, _index, _set[_index]['assigned'])
                    write_attr(graph, _index, _set[_index])
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
                                write_attr(graph, _duplicate, _set[_duplicate])
                                # write_reporter(graph, _duplicate, _set[_duplicate]['reporter'])
                                # write_assigned(graph, _duplicate, _set[_duplicate]['assigned'])
                            flag = True
                        for _depend in _dependson:
                            write_dependson(graph, _index, _depend)
                            if _depend in _set.keys():
                                write_attr(graph, _depend, _set[_depend])
                                # write_reporter(graph, _depend, _set[_depend]['reporter'])
                                # write_assigned(graph, _depend, _set[_depend]['assigned'])
                            flag = True
                        for _block in _blocked:
                            write_blocked(graph, _index, _block)
                            if _block in _set.keys():
                                write_attr(graph, _block, _set[_block])
                                # write_reporter(graph, _block, _set[_block]['reporter'])
                                # write_assigned(graph, _block, _set[_block]['assigned'])
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




