from aiohttp import web
# import app.routes as routes
from app.routes import routes
from app.webSocket import webSocket

app = web.Application()
r = routes(app)
r.setup_routes()
ws = webSocket(app)

if __name__ == '__main__':
    web.run_app(app)
