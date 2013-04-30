
import os
from orun.extjs import *
from orun.servers import cp

class ExtApplication(cp.Application):
    def index(self, *args, **kwargs):
        f = open(os.path.join(os.path.dirname(__file__), 'app.html')).read()
        self.main()
        return f % (self.title, str(js.js_manager))
    index.exposed = True
    
    def ajax_callback(self, *args, **kwargs):
        fn = kwargs.pop('fn')
        if fn:
            fn = js.live_methods[int(fn)]
            fn(*args, **kwargs)
        return str(js.js_manager)
    ajax_callback.exposed = True
    
if __name__ == '__main__':
    app = ExtApplication('Orun (ExtJS Application)')
    app.run()
