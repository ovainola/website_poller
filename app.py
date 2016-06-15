import logging
import platform
from poller import WebPoller, logger_webpoller_factory
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

current_system = platform.system()
if current_system not in ["Windows", "Linux"]:
    raise SystemError("Sorry, could not recognize your system. Terminating program")

webpoller, logger = logger_webpoller_factory("settings.conf", {"main": ["time_period", "pages"],
                                                               "logging": ["settings"]})

@view_config()
def hello(request):
    print(webpoller.poll_results())
    return Response('Hello World')

if __name__ == '__main__':
    config = Configurator()
    config.scan()
    app = config.make_wsgi_app()
    local_url = '0.0.0.0'
    port = 8080
    server = make_server(local_url, port, app)
    print("Starting Pylos server: http://{0}:{1}".format(local_url, port))
    server.serve_forever()
