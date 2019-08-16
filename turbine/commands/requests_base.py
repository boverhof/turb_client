"""
requests_base:  'requests' module drop in replacement

Joshua R. Boverhof, LBNL
See LICENSE.md for copyright notice!
"""
import os,logging,requests,configparser
from requests.exceptions import RequestException, HTTPError, ConnectionError

#def standard_options(url, options, **extra_query):
def read_configuration(configFile, section, **kw):
    """
    http query parameters (kw):
        page
        rpp
        SignedUrl
    """
    assert type(configFile) is configparser.ConfigParser
    assert type(kw.get('SignedUrl', False)) is bool
    params = {}
    url = configFile.get(section, 'url')
    for k,v in kw.items():
        if k == 'subresource' and v:
            url = '/'.join([url.strip('/'),v])
        elif callable(v):
            params[k] = v()
        else:
            params[k] = v
    signed_url = params.get('SignedUrl', False)
    assert type(signed_url) is bool
    verbose =  params.get('verbose', False)
    assert type(verbose) is bool
    rpp =  params.get('rpp', '0')
    assert type(int(rpp)) is int
    pagenum = params.get('page', '0')
    assert type(int(pagenum)) is int
    auth = (configFile.get('Authentication', 'username', raw=True),
        configFile.get('Authentication', 'password', raw=True))
    return (url, auth, params)

def delete_page(configFile, section, **kw):
    url,auth,params = read_configuration(configFile,section,**kw)
    return _delete_page(url, auth, **params).text

def _delete_page(url, auth, **params):
    """
    parameters:
        auth --- username and password tuple
    keyword params
        -- SignedUrl, service will return signed S3 URL and it Will
        automatically be followed.
    """
    assert type(auth) is tuple
    logging.getLogger(__name__).debug('_delete_page url: "%s"', url)
    return requests.delete(url, params=params, auth=auth)

def get_page(configFile, section, **kw):
    url,auth,params = read_configuration(configFile,section,**kw)
    r = _get_page(url, auth, **params)
    return r.text

def _get_page(url, auth, **params):
    """
    parameters:
        auth --- username and password tuple
    keyword params
        -- SignedUrl, service will return signed S3 URL and it Will
        automatically be followed.
    """
    assert type(auth) is tuple
    logging.getLogger(__name__).debug('_get_page url: "%s"', url)
    return requests.get(url, params=params, auth=auth)

def put_page(configFile, section, data, **kw):
    url,auth,params = read_configuration(configFile,section,**kw)
    signed_url = params.get('SignedUrl', False)
    if signed_url is True:
        logging.getLogger(__name__).debug('put_page signed_url: "%s"', url)
        r = _put_page(url, auth, data='', allow_redirects=False, **params)
        assert r.status_code == 302
        url = r.headers.get('Location')
        auth = None
        del params['SignedUrl']
    return _put_page(url, auth, data, **params)

def _put_page(url, auth, **params):
    """
    parameters:
        auth --- username and password tuple
    keyword params
        -- SignedUrl, service will return signed S3 URL and it Will
        automatically be followed.
    """
    assert type(auth) is tuple
    logging.getLogger(__name__).debug('_put_page url: "%s"', url)
    return requests.get(url, params=params, auth=auth)
