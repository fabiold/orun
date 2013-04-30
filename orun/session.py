
class Session(dict):
    def add_object(self, obj):
        self['js_' + id(obj)] = obj

def create_session():
    return Session()
