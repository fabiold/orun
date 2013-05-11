
import types
import json

AJAX_URL = '/ajax_callback'
js_manager = None
js_ajax = None

live_methods = {}

def _encoder(o):
    if isinstance(o, JsObject):
        return o._js
    elif isinstance(o, JsNode):
        return block(str(o))
    elif isinstance(o, types.FunctionType) and js_ajax:
        return function(js_ajax(o))
    
def encode(o):
    if isinstance(o, JsNode):
        return str(o)
    elif isinstance(o, (list, tuple)):
        return '[%s]' % ','.join([encode(i) for i in o])
    else:
        return json.dumps(o, default=_encoder)

# trick json serialize javascript block
class JsBlock(int):
    def __new__(cls, *args, **kwargs):
        obj = super(JsBlock, cls).__new__(cls, 0)
        obj.code = args[0]
        return obj
        
    def __str__(cls):
        return cls.code
    
class JsFunction(JsBlock):
    def __str__(cls):
        return 'function () { %s }' % cls.code

block = JsBlock
func = function = JsFunction

def write(code):
    if js_manager:
        js_manager.write(str(code))
        
    def __lshift__(self, value):
        print('test')

class JsManager(object):
    def __init__(self):
        self.output = []
    
    def write(self, data):
        self.output.append(data)
        
    def __str__(self):
        s = '\n'.join(output)
        output = self.output[:]
        return s
    
class JsNode(object):
    def __init__(self, name='', parent=None):
        if parent and parent.name:
            self.name = parent.name + '.' + name
        else:
            self.name = name

    def __getattr__(self, attr):
        return JsNode(attr, self)
    
    def __setattr__(self, attr, value):
        if attr == 'name':
            super(JsNode, self).__setattr__(attr, value)
        else:
            value = encode(value)
            if self is client.var:
                s = 'var %s = %s' % (attr, value)
            else:
                name = self.name + '.' if self.name else ''
                s = '%s%s = %s' % (name, attr, value)
            write(s)
            
    def __add__(self, other):
        return JsNode('%s + %s' % (encode(self), encode(other)))

    def __sub__(self, other):
        return JsNode('%s - %s' % (encode(self), encode(other)))

    def __mul__(self, other):
        return JsNode('%s * %s' % (encode(self), encode(other)))

    def __truediv__(self, other):
        return JsNode('%s / %s' % (encode(self), encode(other)))

    def __call__(self, *args, **kwargs):
        l = []
        d = []
        for arg in args:
            l.append(encode(arg))
        for k, v in kwargs.items():
            d.append('%s=%s' % (k, encode(v)))
        _args = []
        if l:
            _args.extend(l)
        if d:
            _args.extend(d)
        s = '%s(%s)' % (self.name, ','.join(_args))
        self.name = s
        return self
    
    def __str__(self):
        return self.name
    
class JsClient(JsNode):
    def __init__(self, name='', parent=None):
        if parent and parent.name:
            self.name = parent.name + '.' + name
        else:
            self.name = name
        self.__dict__['var'] = JsNode('var')
        
    def __lshift__(self, other):
        write(other)
        
class JsObjectNode(JsNode):
    def __call__(self, *args, **kwargs):
        super(JsObjectNode, self).__call__(*args, **kwargs)
        write(str(self))

class JsOutput(object):
    def __init__(self, manager=True):
        self.body = []
        if manager:
            js_manager = self
        
    def __lshift__(self, other):
        self.write(other)
        
    def write(self, code):
        self.body.append(code)
        
    def __str__(self):
        s = ';\n'.join(self.body)
        return s
    
out = output = JsOutput

class JsObject(object):
    def __init__(self, *args, **kwargs):
        self._loading = True
        self._id = 'js_%s' % id(self)
        self._create()
        self._js = kwargs
        self._loading = False
        
    def _create(self):
        pass
    
    def _update(self, config):
        self._js.update(config)

    def __getattr__(self, attr):
        if not self.__dict__.get('_loading', True):
            if attr in self._js:
                return self._js.get(attr)
            else:
                return JsObjectNode(attr, JsNode(self._id))
    
    def __setattr__(self, attr, value):
        if '_js' in self.__dict__ and not attr in self.__dict__:
            self[attr] = value
        else:
            super(JsObject, self).__setattr__(attr, value)
        
    def __setitem__(self, attr, value):
        if not self._loading:
            write('%s.%s = %s' % (self._id, attr, json.dumps(value)))
        self._js[attr] = value
        
def alert(msg):
    write(client.alert(msg))

def load(filename, klass=JsObject):
    return klass(**json.load(open(filename)))

cli = client = JsClient()

if __name__ == '__main__':
    class MyManager(JsManager):
        def write(self, code):
            print(code)
    js_manager = MyManager()
    write(client.console.log('test'))
    n = JsNode('console')
    write(n.print(n.log({'id': 'item id'})))
    client.var.x = 1
    client.x.y = client.window.open('http://www.google.com')
    client << client.x.y()([client.x])
    client << client.Ext.create('window', {'left': 10})
    client << client.x
    
    # test block
    print(json.dumps({'click': call}, default=_encoder))
