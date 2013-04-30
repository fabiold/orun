
import cherrypy
from orun import js
from orun import app

class Application(app.Application):
    def index(self):
        return 'Orun application server is running'
    index.exposed = True
    
    def run(self, port=8080, config=None):
        super(Application, self).run()
        cherrypy.quickstart(self, '/', config)

class JsManager(object):
    def write(self, data):
        cherrypy.response.body.append(data)
        
    def __str__(self):
        return ';\n'.join(cherrypy.response.body) + ';'

# Auto start cherrypy javascript manager
js.js_manager = JsManager()

if __name__ == '__main__':
    app = Application()
    app.run()
