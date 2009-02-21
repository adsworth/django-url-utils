from pydoc import classname

from django.db.models import get_model
from django.conf import settings

try:
    import permalinks
    HAS_PERMALINKS = True
except ImportError, e:
    HAS_PERMALINKS = False
    
try:
    NO_APP_GET_ABSOLUTE_URL = settings.NO_APP_GET_ABSOLUTE_URL
except AttributeError:
    NO_APP_GET_ABSOLUTE_URL = False

class NoOverrides(Exception):
    """is thrown if there is no permalinks module available"""
    def __init__(self, msg):
        super(NoOverrides, self).__init__(msg)

class URLResolver(object):
    def __init__(self):
        self.lookup_cache = dict()
        
    def check_configured(self):
        if HAS_PERMALINKS == False:
            raise NoOverrides(u"To use the get_permalink tag create a permalinks module in your PYTHONPATH.")

    def get_app_class(self, app_name):
        cls_inst = getattr(permalinks, app_name, None)

        if cls_inst == None and NO_APP_GET_ABSOLUTE_URL == True:
            raise NoOverrides(u"No %s class in permlainks module." %(app_name))

        return cls_inst

    def get_permalink_callable(self, obj):
        cls_inst = self.get_app_class( obj._meta.app_label )
        meth_name = 'get_%s_url' %(obj._meta.object_name)

        meth_name = meth_name.lower()

        func = getattr(cls_inst, meth_name, None)

        if func == None and NO_APP_GET_ABSOLUTE_URL == True:
            raise NoOverrides(u"No %s classmethod in class %s." %(meth_name, cls_inst.__name__))
        
        return func

    def get_permalink(self, obj):
        self.check_configured()
        func = self.get_permalink_callable(obj)

        if func:
            return func( obj ) 

        return obj.get_absolute_url()


resolver = URLResolver()