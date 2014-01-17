try:
    import simplejson as json
except ImportError:
    import json

from functools import wraps
from twisted.web.server import Site, NOT_DONE_YET
from twisted.python.compat import nativeString
from twisted.web.resource import Resource, NoResource, ErrorPage
from twisted.web._responses import FORBIDDEN, NOT_FOUND

ENCODERS = {
    'application/json' : json.dumps
}
DECODERS = {
    'application/json' : json.loads
}
try:
    import xmltodict
    ENCODERS['application/xml'] = xmltodict.unparse
    DECODERS['application/xml'] = xmltodict.parse
except ImportError:
    pass
# https://github.com/iancmcc/txrestapi/blob/master/txrestapi/resource.py

# encoder
# http://twistedmatrix.com/documents/current/web/howto/using-twistedweb.html#auto7

# web.server.Site
# http://twistedmatrix.com/documents/current/api/twisted.web.server.Site.html
#   def __init__(self, resource, logPath=None, timeout=60 * 60 * 12)

# web.server.Request
# http://twistedmatrix.com/documents/current/api/twisted.web.server.Request.html

# web.resource.Resource / NoResource, ErrorPage, ForbiddenResource, EncodingResourceWrapper
# http://twistedmatrix.com/documents/current/api/twisted.web.resource.Resource.html

DEFAULT_CHARSET = "utf-8"
DEFAULT_CONTENT_TYPE = "application/json"

ErrorPage.template = """{ 
 "code" : %(code)s,
 "message" : "%(brief)s",
 "detail" : "%(detail)s"
}
"""
def middleware(f, content_type=DEFAULT_CONTENT_TYPE, charset=DEFAULT_CHARSET, encoder_=None):
    def setHeader(request):
        request.setHeader(b"content-type", b"%s; charset=%s" % (content_type, charset) )

    @wraps(f)
    def inner(*args, **kwargs):
        request = args[1]
        if request.method in ['POST', 'PUT']:
            decoder = DECODERS.get(request.getHeader('content-type'), lambda s:s)
            request.body = decoder(request.content)
        result = f(*args, **kwargs)
        setHeader(request)
        if result != NOT_DONE_YET:
            encoder = encoder_ if encoder_ != None else ENCODERS.get(content_type, lambda s:s)
            result = encoder(result).encode(charset)
        return result
    return inner

class RestResource(Resource):

    METHODS = [ 'show', 'index', 'create', 'update', 'delete' ]

    def __init__(self, name, module, options={}, children=[]):
        Resource.__init__(self)

        self.name = name
        self.options = options
        self.module = module
        self.cls = self.buildModule(module)
        self.supported = dict([ (m,getattr(self.cls, m)) for m in self.METHODS if hasattr(self.cls, m) ])

        self.rest_children = {}
        for res in children:
            self.rest_children[res[0]] = RestResource(*res)
        if not self.cls:
            for res in children:
                self.putChild(res[0], RestResource(*res))

    def buildModule(self, module):

        if not module:
            return None

        sp = module.split('.')
        try:
            mod = __import__('.'.join(sp[:-1]))
            for m in sp[1:]:
                mod = getattr(mod, m)
        except (ImportError, AttributeError), e:
            return None

        return mod
        #cls = getattr(mod, sp[-1], None)

    def render(self, request):
        if self.cls == None:
            return self.notFound(request, 'module', self.module)

        print 'X', self.cls, request.prepath, request.postpath
        method_name = self.getMethod(request)
        if method_name in self.supported:
            try:
                inst = self.cls(self.options)
            except TypeError:
                inst = self.cls()

            content_type = getattr(inst, 'CONTENT_TYPE', DEFAULT_CONTENT_TYPE)
            charset = getattr(inst, 'CHARSET', DEFAULT_CHARSET)
            return middleware(self.supported[method_name],
                              content_type = content_type, charset = charset) (inst, request)

        return self.notFound(request, 'method', method_name)

#Y xxx ['v1', 'xxx'] ['aa']
#Z aa ['v1', 'xxx'] []
    def getChild(self, path, request):
        print 'YY', path, request.prepath, request.postpath
        if not path: # ends with '/'
            return self

        if not request.postpath or not request.postpath[0]:
            request.args['id'] = path
            return self
            
        request.args['%s_id' % self.name ] = path
        print 'Y', path, request.prepath, request.postpath
        path = request.postpath.pop(0)
        print 'Z', path, request.prepath, request.postpath

        if path in self.rest_children:
            return self.rest_children[path]

        return NoResource(path)

    def getMethod(self, request):
        method = nativeString(request.method)
        name = 'not_found'
        if method == 'GET':
            if 'id' in request.args:
                name = 'show'
            else:
                name = 'index'
        print 'Q', name, request.prepath, request.postpath
        #if name == 'GET'
        #m = getattr(self, 'render_' + nativeString(request.method), None)

        return name

    @middleware
    def notFound(self, request, target, name):
        data = {
            'code' : NOT_FOUND,
            'brief' : "%s not implemented" % target,
            'detail': name
        }
        request.setResponseCode(NOT_FOUND)
        return data

ErrorPage.render = middleware(ErrorPage.render, encoder_=lambda s:s)

class RootResource(Resource):

    def __init__(self, path = '/', resources = []):
        Resource.__init__(self)

        self.path = [p for p in path.split('/') if p]
        for res in resources:
            self.putChild(res[0], RestResource(*res))

    def getChild(self, path, request):
        for p in self.path:
            if p != path:
                return NoResource()
            path = request.postpath.pop(0)

        if path in self.children:
            return self.children[path]
        
        return NoResource(path)

def build(root_path, paths):
    root = RootResource(root_path, paths)

    return Site(root);
