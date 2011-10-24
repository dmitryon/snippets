import datetime


def _walker(d, checker):
    """Walks through values of lists, dicts (including nested)
    and replaces it with possible values returned by checker.
    """
    if isinstance(d, dict):
        for key, value in d.iteritems():
            if isinstance(value, (tuple, list, dict)):
                d[key] = _walker(value, checker)
            else:
                try:
                    result = checker(value)
                    d[key] = result
                except:
                    continue
        return d
    elif isinstance(d, (list, tuple)) or hasattr(d, '__iter__'):
        new_list = []
        for value in d:
            if isinstance(value, (tuple, list, dict)):
                new_list.append(_walker(value, checker))
            else:
                try:
                    result = checker(value)
                    new_list.append(result)
                except:
                    new_list.append(value)
        return tuple(new_list) if isinstance(d, tuple) else new_list
    else:
        #single value
        try:
            return checker(d)
        except:
            return d


def encode_datetime(d):
    return d.strftime("%Y-%m-%d %H:%M:%S")


def json_safe(values):
    """Prepares common python structure for json.dumps().

    Converts dictionaries returned by QuerySet.values() into json-safe values:
    datetime.datetime -> iso string
    decimal.Decimal -> string with decimal float
    """
    def _checker(value):
        from decimal import Decimal
        if isinstance(value, datetime.datetime):
            result = encode_datetime(value)
        elif isinstance(value, Decimal):
            result = str(value)
        elif isinstance(value, (list, tuple, dict)):
            result = json_safe(value)
        else:
            raise ValueError
        return result

    return _walker(values, _checker)



def _unicode(value):
    if isinstance(value, str):
        return value.decode("utf-8")
    assert isinstance(value, unicode)
    return value


def unicode_safe(values):
    """Converts all strings occurences in list or dict into unicode."""
    return _walker(values, _unicode)
