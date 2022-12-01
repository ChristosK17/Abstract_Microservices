from functools import wraps
from flask import request, abort
import ssl

path = "C://Users//ckiokak//Documents//Abstract_Microservices//api_key_protection//"
context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)
context.load_cert_chain(path+'server.crt', path+'server.key')

# The actual decorator function
def require_appkey(view_function):
    @wraps(view_function)
    # the new, post-decoration function. Note *args and **kwargs here.
    def decorated_function(*args, **kwargs):
        with open(path+'api.key', 'r') as apikey:
            key=apikey.read().replace('\n', '')
        #if request.args.get('key') and request.args.get('key') == key:
        if request.headers.get('x-api-key') and request.headers.get('x-api-key') == key:
            return view_function(*args, **kwargs)
        else:
            raise Exception("Incorrect API key")
    return decorated_function