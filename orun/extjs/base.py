
import json
from . import js

__all__ = ['create', 'createByAlias', 'Component']

def js_ajax(fn):
    i = id(fn)
    js.live_methods[i] = fn
    return js.client.Ext.Ajax.request({'url': js.AJAX_URL, 'method': 'GET', 'params': {'fn': i, 'id': js.client.this.id}, 'success': js.function('eval(arguments[0].responseText);')})

js.js_ajax = js_ajax

def _create(meth, name, args):
    #args['pyLive'] = True : TODO
    obj = Component(**args)
    js.write('var %s = Ext.create("%s", %s);' % (obj._id, name, str(obj)))
    return obj

def create(name, args={}):
    return _create('create', name, args)

def createByAlias(alias, args={}):
    return _create('createByAlias', alias, args)

def get(id):
    return js.JsNode('Ext.get("%s")' % id)

def getCmp(id):
    return js.JsNode('Ext.getCmp("%s")' % id)

class Component(js.JsObject):
    def __init__(self, *args, **kwargs):
        super(Component, self).__init__(*args, **kwargs)
        
    def _update(self, config):
        def get_obj(value):
            if isinstance(value, dict):
                return Component(**v)
            elif isinstance(value, (list, tuple)):
                return [get_obj(v) for v in value]
            else:
                return value
        cfg = {}
        for k, v in config.items():
            cfg[k] = get_obj(v)
        super(Component, self).update(cfg)
        
    def down(self, item):
        pass
    
    def up(self, item):
        pass
    
    def __str__(self):
        return json.dumps(self._js, default=js._encoder)
