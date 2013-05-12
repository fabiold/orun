
def TAG(tag='html', *args, **kwargs):
    s = '<' + tag
    for key in kwargs:
        value = kwargs[key]
        if key[0] == '_':
            key = key[1:]
        s += ' %s="%s"' % (key, value)
    if len(args) == 0:
        s += ' />'
    else:
        s += '>'
        for value in args:
            s += value
        s += '</%s>' % tag
    return s

def HTML(*args, **kwargs):
    return TAG('html', *args, **kwargs)

def BODY(*args, **kwargs):
    return TAG('body', *args, **kwargs)

def BUTTON(*args, **kwargs):
    value = kwargs.pop('value', '')
    value = kwargs.pop('_value', value)
    args = list(args)
    args.append(value)
    return TAG('button', *args, **kwargs)

def BR():
    return '<br/>'

def CENTER(*args, **kwargs):
    return TAG('center', *args, **kwargs)

def DIV(*args, **kwargs):
    return TAG('div', *args, **kwargs)

def FORM(*args, **kwargs):
    return TAG('form', *args, **kwargs)

def INPUT(*args, **kwargs):
    return TAG('input', *args, **kwargs)

def LABEL(*args, **kwargs):
    value = kwargs.pop('value', '')
    value = kwargs.pop('_value', value)
    args = list(args)
    args.append(value)
    return TAG('label', *args, **kwargs)

def OPTION(*args, **kwargs):
    value = kwargs.pop('value', '')
    args = list(args)
    args.append(value)
    return TAG('option', *args, **kwargs)

def SELECT(*args, **kwargs):
    value = kwargs.pop('value', '')
    values = kwargs.pop('values', [])
    args = list(args)
    args.append(value)
    for key in values:
        args.append(OPTION(value=key))
    return TAG('select', *args, **kwargs)

def SCRIPT(*args, **kwargs):
    value = kwargs.pop('value', '')
    args = list(args)
    args.append(value)
    return TAG('script', *args, **kwargs)

def LINK(*args, **kwargs):
    value = kwargs.pop('value', '')
    args = list(args)
    args.append(value)
    return TAG('link', *args, **kwargs)

def TABLE(*args, **kwargs):
    return TAG('table', *args, **kwargs)

def TD(*args, **kwargs):
    return TAG('td', *args, **kwargs)

def TH(*args, **kwargs):
    return TAG('th', *args, **kwargs)

def TR(*args, **kwargs):
    return TAG('tr', *args, **kwargs)

def ToHTML(obj, table=False):
    rows = []
    if isinstance(obj, (list, tuple, dict)):
        for row in obj:
            rows.append(TR(TD(str(row))))
    else:
        return str(obj)
    if table:
        return TABLE(*rows)
