from aiohttp import web
from app.routes import routes
from app.webSocket import webSocket

app = web.Application()
app.ws = webSocket(app)
r = routes(app)
r.setup_routes()

if __name__ == '__main__':
    web.run_app(app)
