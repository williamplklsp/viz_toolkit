from gevent.pywsgi import WSGIServer
from app import app

if __name__ == "__main__":
    # only 8000 Byte URL limit
    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()
