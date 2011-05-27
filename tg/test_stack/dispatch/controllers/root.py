# -*- coding: utf-8 -*-

import tg, pylons
from tg.controllers import TGController, CUSTOM_CONTENT_TYPE
from tg.decorators import expose, validate, paginate
from formencode import validators

from tg import expose, redirect, config
from tg.controllers import TGController, RestController
from nose.tools import eq_

class DomainController(RestController): 
        def __init__(self): 
                self._domains = {} 
                self._domains["do.com"] = "do.com" 
                self._domains["dom.com"] = "dom.com" 
                self._domains["doma.com"] = "doma.com" 
                self._domains["domain.com"] = "domain.com" 
        @expose() 
        def get_one(self, domain_id): 
                print "in get_one" 
                return "you can not do anything with [%s] now" % (domain_id) 
        @expose() 
        def get_all(self, **dict): 
                str_domain_ids = ""
                for domain_id in self._domains.keys(): 
                    str_domain_ids += "[%s] " % (domain_id) 
                return str_domain_ids 

class SubController(object):
    @expose()
    def foo(self,):
        return 'sub_foo'

    @expose()
    def index(self):
        return 'sub index'

    @expose()
    def default(self, *args):
        return ("recieved the following args (from the url): %s" %list(args))

    @expose()
    def redirect_me(self, target, **kw):
        tg.redirect(target, **kw)

    @expose()
    def redirect_sub(self):
        tg.redirect('index')
    
    @expose()
    def redirect_list(self):
        tg.redirect(["/sub2", "list"])

    @expose()
    def hello(self, name):
        return "Why HELLO! " + name

class LookupController(TGController):
    @expose()
    def findme(self, *args, **kw):
        return 'got to lookup'

class SubController2(object):
    @expose()
    def index(self):
        tg.redirect('list')

    @expose()
    def list(self, **kw):
        return "hello list"

    @expose()
    def lookup(self, *args):
        lookup = LookupController()
        return lookup, args

class RootController(TGController):
    @expose()
    def index(self, **kwargs):
        return 'hello world'

    @expose()
    def default(self, remainder):
        return "Main Default Page called for url /%s"%remainder

    @expose()
    def feed(self, feed=None):
        return feed

    sub = SubController()
    sub2 = SubController2()
    dom = DomainController()

    @expose()
    def redirect_me(self, target, **kw):
        tg.redirect(target, kw)

    @expose()
    def hello(self, name, silly=None):
        return "Hello " + name

    @expose()
    def redirect_cookie(self, name):
        pylons.response.set_cookie('name', name)
        tg.redirect('/hello_cookie')

    @expose()
    def hello_cookie(self):
        return "Hello " + pylons.request.cookies['name']

    @expose()
    def flash_redirect(self):
        tg.flash("Wow, flash!")
        tg.redirect("/flash_after_redirect")

    @expose()
    def flash_unicode(self):
        tg.flash(u"Привет, мир!")
        tg.redirect("/flash_after_redirect")

    @expose()
    def flash_after_redirect(self):
        return tg.get_flash()

    @expose()
    def flash_status(self):
        return tg.get_status()

    @expose()
    def flash_no_redirect(self):
        tg.flash("Wow, flash!")
        return tg.get_flash()

    @expose('json')
    @validate(validators={"some_int": validators.Int()})
    def validated_int(self, some_int):
        assert isinstance(some_int, int)
        return dict(response=some_int)

    @expose('json')
    @validate(validators={"a":validators.Int()})
    def validated_and_unvalidated(self, a, b):
        assert isinstance(a, int)
        assert isinstance(b, unicode)
        return dict(int=a,str=b)

    @expose()
    @expose('json')
    def stacked_expose(self, tg_format=None):
        return dict(got_json=True)

    @expose(content_type='image/png')
    def custom_content_type(self):
        return 'PNG'
    
    @expose(content_type='text/plain')
    def custom_content_text_plain_type(self):
        return 'a<br/>bx'

    @expose(content_type=CUSTOM_CONTENT_TYPE)
    def custom_content_type2(self):
        pylons.response.headers['Content-Type'] = 'image/png'
        return 'PNG2'
    
    @expose()
    def check_params(self, *args, **kwargs):
        if not args and not kwargs:
            return "None recieved"
        else:
            return "Controler recieved: %s, %s" %(args, kwargs) 
    
    @expose()
    def test_url_sop(self):
        from tg import url
        eq_('/foo', url('/foo'))

        
        u = url("/foo", bar=1, baz=2)
        assert u in \
                ["/foo?bar=1&baz=2", "/foo?baz=2&bar=1"], u

    @expose('json')
    @paginate('nothing')
    def paginated_positional_args(self, alpha, beta=None, **kwargs):
        result = dict()
        for x in kwargs:
            result[x] = kwargs[x]
        result['alpha'] = alpha
        result['beta'] = beta
        return result

