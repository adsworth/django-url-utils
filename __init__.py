from pydoc import classname

from django.db.models import get_model
from django.conf import settings

try:
    import url_overrides
    HAS_OVERRIDES = True
except ImportError, e:
    HAS_OVERRIDES = False
    
try:
    NO_APP_GET_ABSOLUTE_URL = settings.NO_APP_GET_ABSOLUTE_URL
except AttributeError:
    NO_APP_GET_ABSOLUTE_URL = False

class NoOverrides(Exception):
    """is thrown if there is no url_overrides module available"""
    def __init__(self, msg):
        super(NoOverrides, self).__init__(msg)

class URLResolver(object):
    def __init__(self):
        self.lookup_cache = dict()
        
    def check_configured(self):
        if HAS_OVERRIDES == False:
            raise NoOverrides(u"To use the get_url tag create a url_overrides module in your PYTHONPATH.")

    def get_app_class(self, app_name):
        cls_inst = getattr(url_overrides, app_name, None)

        if cls_inst == None and NO_APP_GET_ABSOLUTE_URL == True:
            raise NoOverrides(u"No %s class in url_overrides module." %(app_name))

        return cls_inst

    def get_override_callable(self, obj):
        cls_inst = self.get_app_class( obj._meta.app_label )
        meth_name = 'get_%s_url' %(obj._meta.object_name)

        meth_name = meth_name.lower()

        func = getattr(cls_inst, meth_name, None)

        if func == None and NO_APP_GET_ABSOLUTE_URL == True:
            raise NoOverrides(u"No %s classmethod in class %s." %(meth_name, cls_inst.__name__))
        
        if func:
            obj_url = func( obj )
        else:
            obj_url = obj.get_absolute_url()

        return obj_url

    def get_url(self, obj):
        self.check_configured()
        meth = self.get_override_callable(obj)
        return meth


resolver = URLResolver()