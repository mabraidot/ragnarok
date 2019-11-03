from aiohttp import web
import aiohttp_cors
from app.routes import routes
from app.webSocket import webSocket

app = web.Application()
r = routes(app)
r.setup_routes()
ws = webSocket(app)


# Configure default CORS settings.
cors = aiohttp_cors.setup(app, defaults={
    "*": aiohttp_cors.ResourceOptions(
            allow_credentials=True,
            expose_headers="*",
            allow_headers="*",
        )
})
# Configure CORS on all routes.
for route in list(app.router.routes()):
    cors.add(route)


if __name__ == '__main__':
    web.run_app(app)
