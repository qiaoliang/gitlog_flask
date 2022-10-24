def obj2json(obj, atom_type: list = None, collect_type: list = None) -> str:
    def _obj2dict(in_obj, dc: dict, _atom_type, _collect_type):
        if isinstance(in_obj, dict):
            dict_obj = in_obj
        else:
            dict_obj = in_obj.__dict__
        for key, value in dict_obj.items():
            if value is None:
                dc[key] = None
            elif isinstance(value, _atom_type):
                dc[key] = value
            elif isinstance(value, dict):
                dc[key] = dict()
                _obj2dict(value, dc[key], _atom_type, _collect_type)
            elif isinstance(value, _collect_type):
                dc[key] = list()
                for item in value:
                    sub_dc = dict()
                    _obj2dict(item, sub_dc, _atom_type, _collect_type)
                    dc[key].append(sub_dc)
            else:
                dc[key] = dict()
                _obj2dict(value, dc[key], _atom_type, _collect_type)

    ret = dict()
    if not atom_type:
        _atom_type = (int, float, str, bool, bytes)
    else:
        _atom_type = tuple(set(atom_type + [int, float, str, bool, bytes]))
    if not collect_type:
        _collect_type = (set, tuple, list)
    else:
        _collect_type = tuple(set(collect_type + [set, tuple, list]))
    _obj2dict(obj, ret, _atom_type, _collect_type)
    return ret