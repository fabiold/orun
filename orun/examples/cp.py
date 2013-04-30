
from orun.extjs import *
from orun.extjs import cp

def ok_click(id, *args, **kwargs):
    cli << Ext.getCmp(id).setText('Clicked')
    cli << js.client.alert('Server side message')

def button_click(id, *args, **kwargs):
    js.write("""
    Ext.getCmp("%s").setText('Clicked');
    alert('Server side callback message');
    """ % id)

class MyApplication(cp.ExtApplication):
    def main(self, *args, **kwargs):
        wnd = Ext.create('widget.window', {'title': 'My Window', 'width': 300, 'height': 250,
            'items': [{'xtype': 'button', 'text': 'Click Here', 'handler': button_click}],
            'buttons': [
                {'text': 'OK', 'handler': ok_click},
                {'text': 'Close', 'handler': js.function('this.up("window").close();')}]})
        wnd.show()
        wnd.setHeight(200)

app = MyApplication('Orun (ExtJS Application)')
app.run()
