import unicodedata
import urllib


def normalize(name):
    if not isinstance(name, unicode):
        name = name.decode('utf-8')

    name = name.replace("'", '')
    return unicodedata.normalize('NFKC', name).encode('utf-8')


def quote(name):
    if isinstance(name, unicode):
        name = normalize(name)

    return urllib.quote(name)


def make_icon_url(region, icon, size='large'):
    if not icon:
        return ''

    if size == 'small':
        size = 18
    else:
        size = 56

    # http:// <region> + .battle.net/static-render/ + <region> + / + <the string you got from API as thumbnail> 
    return 'http://%s.battle.net/static-render/%s/%s.jpg' % (region, region, icon)


def make_connection():
    if not hasattr(make_connection, 'Connection'):
        from .connection import Connection
        make_connection.Connection = Connection

    return make_connection.Connection()
