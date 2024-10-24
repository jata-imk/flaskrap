from werkzeug.middleware.proxy_fix import ProxyFix
from app import create_app

app = create_app()

app.wsgi_app = ProxyFix(
    app.wsgi_app, x_for=2, x_proto=2, x_host=2, x_prefix=2
)

if __name__ == '__main__':
    app.run()