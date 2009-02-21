from url_utils import resolver
from django import template


register = template.Library()


class URLResolverNode(template.Node):
    def __init__(self, obj):
        self.obj_var = template.Variable( obj )
    
    def render(self, context):
        return resolver.get_permalink( self.obj_var.resolve( context ) )

def get_permalink(parser, token):
    """
    get a project specific url of the object or the default get_absolute_url.
    
    Syntax::
    
        {% get_permalink object %}
    
    Example::
    
        {% get_permalink entry %}
    
    """
    bits = token.contents.split()
    if len(bits) != 2:
      raise template.TemplateSyntaxError("'%s' tag takes one arguments" % bits[0])
    return URLResolverNode( bits[1] )

register.tag('get_permalink', get_permalink)
