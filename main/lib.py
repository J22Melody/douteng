from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.utils.safestring import mark_safe
from django.utils.decorators import available_attrs
from django.utils import simplejson
from functools import wraps

_ERROR_MSG = '<!DOCTYPE html><html lang="en"><body><h1>%s</h1><p>%%s</p></body></html>'
_400_ERROR = _ERROR_MSG % '400 Bad Request'
_403_ERROR = _ERROR_MSG % '403 Forbidden'
_405_ERROR = _ERROR_MSG % '405 Not Allowed'


"""
usage:
    @ajax_view
    def foo():

or 
    @ajax_view(option)
    def foo():
"""


def ajax_view(function=None, FormClass=None, method="GET", login_required=True, ajax_required=True, json_form_errors=False):    
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _ajax_view(request, *args, **kwargs):
            if request.method != method and method != 'REQUEST':
                return HttpResponseNotAllowed(mark_safe(_405_ERROR % ("Request must be a %s." % method)))
            if ajax_required and not request.is_ajax():
                return HttpResponseForbidden(mark_safe(_403_ERROR % "Request must be set via AJAX."))
            if login_required and not request.user.is_authenticated():
                return HttpResponseForbidden(mark_safe(_403_ERROR % "Login required"))

            if FormClass:
                f = FormClass(getattr(request, method))
                    
                if not f.is_valid():
                    if json_form_errors:
                        errors = dict((k, [unicode(x) for x in v]) for k,v in f.errors.items())
                        return HttpResponse(simplejson.dumps({'error': 'form', 'errors': errors}), 'application/json')
                    else:   
                        return HttpResponseBadRequest(mark_safe(_400_ERROR % ('Invalid form<br />' + f.errors.as_ul())))
                request.form = f
            return view_func(request, *args, **kwargs)
        return _ajax_view
            
    if function:
        return decorator(function)
    return decorator